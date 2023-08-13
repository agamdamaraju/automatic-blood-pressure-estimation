import h5py, os, time, shutil
from os.path import join
from scipy.signal import butter, filtfilt
import librosa, matplotlib.pyplot as p
import numpy as np

fdr = 1
os.chdir("F:")
trigger = False
for fol in os.listdir(join('bp_transfer', 'rawData')):
    print(f"Processing folder:{fol}, count:{fdr}")
    fl = 1
    for file in os.listdir(join('bp_transfer', 'rawData', fol)):
        try:
            if file == "3013765_0012.h5":
                s = time.time()
                with h5py.File(join('bp_transfer', 'rawData', fol, file), 'r') as f:
                    j = True
                    data = {}
                    for key in f.keys():
                        data[key] = np.array(f[key]).transpose()
                    isnan = np.isnan(data['val'][0])
                    nan_abp_idx = np.where(np.isnan(data['val'][0]))
                    if len(nan_abp_idx[0])>0:
                        aa1 = np.delete(data['val'][0], nan_abp_idx[0])
                        bb1 = np.delete(data['val'][1], nan_abp_idx[0])
                    else:
                        aa1 = data['val'][0]
                        bb1 = data['val'][1]
                    nan_ppg_idx = np.where(np.isnan(bb1))
                    if len(nan_ppg_idx[0])>0:
                        aa = np.delete(aa1, nan_ppg_idx[0])
                        bb = np.delete(bb1, nan_ppg_idx[0])
                    else:
                        aa = aa1
                        bb = bb1
                    b,a = butter(4, 5, 'lowpass', fs=125)
                    e, f = butter(4, 8, 'lowpass', fs=125)
                    i, j = butter(3, 5, 'highpass', fs=125)
                    # e,f = butter(4, [0.1, 8], 'bandpass', fs=125)
                    abp = filtfilt(b, a, aa)
                    cc = filtfilt(e, f,bb)
                    ppg = filtfilt(i, j, cc)
                    p.plot(ppg)
                    p.show()
                    break
                    res2 = np.where(np.isnan(ppg))
                    abp_down_sampled = librosa.resample(abp, orig_sr=125, target_sr=30)
                    ppg_down_sampled = librosa.resample(ppg, orig_sr=125, target_sr=30)
                    i = 0
                    while (i+8)*30 < abp_down_sampled.__len__():
                        win_abp = abp_down_sampled[i*30: (i+8)*30]
                        win_ppg = ppg_down_sampled[i*30: (i+8)*30]
                        if j:
                            ppg_data = win_ppg
                            abp_data = win_abp
                        else:
                            ppg_data = np.dstack((ppg_data, win_ppg))
                            abp_data = np.dstack((abp_data, win_abp))
                        i += 6
                        j = False
                e = time.time()
                print(f"File:{file}, file_count:{fl}, folder_count:{fdr}, processed in {e-s} seconds.")
                fl += 1
                np.save('test_ppg.npy', ppg_data)
                trigger=True
                break
        #     np.save(join('Dataset', 'Output', f"{file[:-3]}_ppg.npy"), ppg_data)
        #     np.save(join('Dataset', 'Output', f"{file[:-3]}_abp.npy"), abp_data)
        except Exception as e:
            print(f"Error in file {file}: {e}")
            # #break
            # if not os.path.isdir(join('Dataset', 'Failed')):
            #     os.mkdir(join('Dataset', 'Failed'))
            # shutil.move(join('Dataset', 'rawData', fol, file), join('Dataset', 'Failed'))
    # if fdr == 5:
    #     break
    # fdr += 1
    if trigger:
        break
# ppg_data = np.reshape(ppg_data, (ppg_data.shape[1], ppg_data.shape[2]))
# abp_data = np.reshape(abp_data, (abp_data.shape[1], abp_data.shape[2]))
# np.save(join("Output","PPG.npy"), ppg_data)
# np.save(join("Output","ABP.npy"), abp_data)