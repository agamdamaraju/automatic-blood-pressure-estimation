import os, numpy as np, matplotlib.pyplot as p, time, heartpy as hp
from itertools import compress
from scipy.signal import butter, filtfilt
def find_minima(sig, pks, fs):
    min_pks = []
    for i in range(0,len(pks)): 
        pks_curr = pks[i]
        if i == len(pks)-1:
            pks_next = len(sig)
        else:
            pks_next = pks[i+1]

        sig_win = sig[pks_curr:pks_next]
        if len(sig_win) < 1.5*fs:
            min_pks.append(np.argmin(sig_win) + pks_curr)
    return min_pks

def abpp(wave):
    sys = []
    dia = []
    abp_FidPoints = hp.process(wave, 30)
    ValidPks = abp_FidPoints[0]['binary_peaklist']
    abp_sys_pks = abp_FidPoints[0]['peaklist']
    abp_sys_pks = list(compress(abp_sys_pks, ValidPks == 1))
    abp_dia_pks = find_minima(wave, abp_sys_pks, 30)
    for i in abp_sys_pks:
        sys.append(wave[i])
    for i in abp_dia_pks:
        dia.append(wave[i])
    return np.array([np.median(dia), np.median(sys)])

# os.chdir("G:")

# for fol in os.listdir(os.path.join("Dataset", "finalOutput")):
#     file = 1
#     for idx in range(0, len(os.listdir(os.path.join("Dataset", "finalOutput", fol))), 2):
#         abp_file = os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx]
#         ppg_file = os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx+1]
#         if abp_file.split('abp')[0] == ppg_file.split('ppg')[0]:
#             abp_signal = np.load(os.path.join('Dataset', 'finalOutput', fol, abp_file))
#             ppg_signal = np.load(os.path.join('Dataset', 'finalOutput', fol, ppg_file))
#             print("ABP shape:", abp_signal.shape)
#             print("PPG shape:", ppg_signal.shape)
#             i = 0
#             while True:
#                 if not i >= abp_signal.shape[-1]:
#                     # if np.std(ppg_signal[0, :, i]) >= 0.55 or np.std(abp_signal[0,:,i]) < 10.0 or len(abp_signal[0, :, i][abp_signal[0, :, i]>=25]) != 240 or len(abp_signal[0, :, i][abp_signal[0, :, i]<=140]) != 240:
#                     if np.min(abp_signal[0,:,i]) < 30 or np.max(abp_signal[0,:,i]) > 200:
#                         abp_signal = np.delete(abp_signal, i, 2)
#                         ppg_signal = np.delete(ppg_signal, i, 2)
#                     else:
#                         try:
#                             abpp(abp_signal[0,:,i])
#                             a, j = butter(3, 5, 'highpass', fs=125)
#                             ppg_signal[0, :, i] = filtfilt(a, j, ppg_signal[0, :, i])
#                             abp_signal[0, :, i] = abp_signal[0, :, i] - 30
#                             abp_signal[0, :, i] = abp_signal[0, :, i] / 170
#                             if np.min(ppg_signal[0,:,i]) < 0:
#                                 ppg_signal[0, :, i] = ppg_signal[0, :, i] + np.abs(np.min(ppg_signal[0, :, i]))
#                             ppg_signal[0, :, i] = (ppg_signal[0, :, i] - np.min(ppg_signal[0, :, i])) / (np.max(ppg_signal[0, :, i]) - np.min(ppg_signal[0, :, i]))
#                             i += 1
#                         except:
#                             abp_signal = np.delete(abp_signal, i, 2)
#                             ppg_signal = np.delete(ppg_signal, i, 2)
#                 else:
#                     print(f"ABP signal shape: {abp_signal.shape}")
#                     print(f"PPG signal shape: {ppg_signal.shape}")
#                     break
#             if file > 2:
#                 ppg_data = np.dstack((ppg_data, ppg_signal))
#                 abp_data = np.dstack((abp_data, abp_signal))
#             else:
#                 ppg_data = ppg_signal
#                 abp_data = abp_signal
#             print(f"ABP stacked shape: {abp_data.shape}")
#             print(f"PPG stacked shape: {ppg_data.shape}")
#             # p.plot(ppg_data[0, :, :])
#             # p.show()
#             # p.plot(abp_data[0, :, :])
#             # p.show()
#             np.save(os.path.join("Dataset", "finalData", f"finalPPGData_{fol}.npy"), ppg_data)
#             np.save(os.path.join("Dataset", "finalData", f"finalABPData_{fol}.npy"), abp_data)
#             with open(os.path.join('Dataset', 'finalData','status.txt'), 'w') as f:
#                 f.write(f"{os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx]}\n")
#                 f.write(f"{os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx+1]}")
#             print(f"abp and ppg files {os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx]} and {os.listdir(os.path.join('Dataset', 'finalOutput', fol))[idx+1]}, count: {fol}/{file}/{file+1} processed.")
#             file += 2
#         else:
#             print(f"Different files, Skipping: {abp_file} and {ppg_file} in {fol}")
#
# print("DONE ALL!!!!!")

############ Cleaning stage-2 ################################
for fol in os.listdir(os.path.join("Dataset", "finalData")):
    abp = np.load(os.path.join("Dataset", "finalData", fol, f"finalABPData_set_{fol}.npy"))
    ppg = np.load(os.path.join("Dataset", "finalData", fol, f"finalPPGData_set_{fol}.npy"))
    if abp.shape[2] == ppg.shape[2]:
        print(f'Processing folder: {fol}...')
        with open(os.path.join('Dataset', 'finalData', 'status.txt'), 'a') as f:
            f.write(f"Before Folder: {fol}, ABP shape: {abp.shape}\n")
            f.write(f"Before Folder: {fol}, PPG shape: {ppg.shape}\n")
        i = 0
        while True:
            if not i >= abp.shape[-1]:
                if True in np.isnan(abp[0,:,i]) or True in np.isnan(ppg[0,:,i]):
                    abp = np.delete(abp, i, 2)
                    ppg = np.delete(ppg, i, 2)
                else:
                    try:
                        abpp(abp[0, :, i])
                        i += 1
                    except:
                        abp = np.delete(abp, i, 2)
                        ppg = np.delete(ppg, i, 2)
                # print(abp.shape, ppg.shape)
            else:
                break
        np.save(os.path.join("Dataset", "finalData", fol, f"finalABPData_set_{fol}.npy"), abp)
        np.save(os.path.join("Dataset", "finalData", fol, f"finalPPGData_set_{fol}.npy"), ppg)
        with open(os.path.join('Dataset', 'finalData', 'status.txt'), 'a') as f:
            f.write(f"After Folder: {fol}, ABP shape: {abp.shape}\n")
            f.write(f"After Folder: {fol}, PPG shape: {ppg.shape}\n")
    else:
        with open(os.path.join('Dataset', 'finalData', 'status.txt'), 'a') as f:
            f.write(f"ABP and PPG shapes are not equal in folder {fol}\n")
    print(f"Folder: {fol} processed.")
print("DONE!!!")

####################
# abp = np.load(os.path.join("Dataset", "finalData", "2", "finalABPData_set_2.npy"))
# plt.plot(abp[0,:,26630])
# plt.show()
# try:
#     abpp(abp[0,:,26631])
# except:
#     print("Exception")


#################################### Non usable code #################################################
# ppg_data.shape
#
# ppg_data = np.dstack((ppg_data_1, ppg_data_2))
# abp_data = np.dstack((abp_data_1, abp_data_2))
# print(abp_data.shape, ppg_data.shape)
#
# # #####################################################################################################################
# test_abp = abp_data
# test_ppg = ppg_data
# i = 0
# while True:
#     if not i>=abp_data.shape[2]:
#     # if not i>=15000:
#         try:
#             # abp_peaks = abp(abp_data[0, :, i])
#             # if True in np.isnan(abp_peaks):
#             #     abp_data = np.delete(abp_data, i, 2)
#             #     ppg_data = np.delete(ppg_data, i, 2)
#             # else:
#             # abp_peaks_log = np.log10(abp(abp_data[0, :, i]))
#             abp_peaks_log = np.log10(abp_data[0, :, i])
#             if i > 0:
#                 # updated_abp = np.dstack((updated_abp, abp_peaks))
#                 updated_abp_log = np.dstack((updated_abp_log, abp_peaks_log))
#             else:
#                 # updated_abp = abp_peaks
#                 updated_abp_log = abp_peaks_log
#             # print(f"ABP stacked shape: {updated_abp.shape}")
#             print(f"ABP stacked log shape: {updated_abp_log.shape}")
#             print(f"abp, ppg shape: {abp_data.shape, ppg_data.shape}")  ##  67.08394249, 125.7916337
#             i+=1
#         except:
#             abp_data = np.delete(abp_data, i, 2)
#             ppg_data = np.delete(ppg_data, i, 2)
#     else:
#         break
# #936945
#
# # ###############################################################################################################
# abp_data = np.load(os.path.join('finalData','stacked_data', 'ABP.npy'))
# ppg_data = np.load(os.path.join('finalData','stacked_data', 'PPG.npy'))
# print(ppg_data.shape, abp_data.shape)
# plt.plot(abp_data[0,:,2539])
# plt.show()
# abp_data_1 = abp_signal[:,:,:]
# # ppg_data_1 = ppg_data[:,:,:1000000]
# # abp_data_test = abp_data[:,:,2000:]
# # ppg_data_2 = ppg_data[:,:,1000000:1002000]
# # abp_data_3 = abp_data[:,:,2000000:]
# # ppg_data_3 = ppg_data[:,:,2000000:]
# p.plot(abp_signal[0,:,:])
# p.show()
#
# p.plot(ppg_signal[0,:,:])
# p.show()
# # print(abp_data_1.shape[2]+abp_data_2.shape[2]+abp_data_3.shape[2])
# # print(ppg_data_1.shape[2]+ppg_data_2.shape[2]+ppg_data_3.shape[2])
# i = 0
# # l = [] ###3240607
# # new = abp_data_test[:,:,-100:]
# # new_2 = new
# while True:
#     if not i >= abp_data_1.shape[2]:
#         # if len(abp_data[0, :, i][abp_data[0, :, i]<=3]) != 240 or len(abp_data[0, :, i][abp_data[0, :, i]<=-3]) != 240:
#         if np.std(abp_data_1[0,:,i]) < 10.0 or len(abp_data_1[0, :, i][abp_data_1[0, :, i]>=25]) != 240 or len(abp_data_1[0, :, i][abp_data_1[0, :, i]<=140]) != 240:
#             # print('$$$$', i)
#             abp_data_1 = np.delete(abp_data_1, i, 2)
#             # print('std', np.std(abp_data_2[0,:,i]), i)
#             # time.sleep(3)
#             # ppg_data = np.delete(ppg_data, i, 2)
#         else:
#             print(i)
#             i += 1
#     else:
#         break
#
# ##############################################################
# #3241584
# np.save(os.path.join("finalData","stacked_data","PEAKS_ABP.npy"), updated_abp)
# np.save(os.path.join("finalData","stacked_data","LOG10_PEAKS_ABP.npy"), updated_abp_log)
# np.save(os.path.join("finalData","stacked_data","PEAKS_PPG.npy"), ppg_data)
# np.save(os.path.join("finalData","stacked_data","ABP.npy"), abp_data)
# np.save(os.path.join("finalData","stacked_data","PPG.npy"), ppg_data)
# # abp_data = np.reshape(abp_data, (abp_data.shape[2], abp_data.shape[1], abp_data.shape[0]))
# # ppg_data = np.reshape(ppg_data, (ppg_data.shape[2], ppg_data.shape[1], ppg_data.shape[0]))
# # np.save(os.path.join("finalData","PPG_2.npy"), ppg_data)
# # np.save(os.path.join("finalData","ABP_2.npy"), abp_data)
