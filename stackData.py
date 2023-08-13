import numpy as np, os
for fol in os.listdir(os.path.join("Dataset", "done")):
    trigger = True
    idx = 2
    while True:
        if trigger:
            file_stacked = np.load(os.path.join("Dataset", "done", fol, os.listdir(os.path.join("Dataset", "done", fol))[0]))
            file = np.load(os.path.join("Dataset", "done", fol, os.listdir(os.path.join("Dataset", "done", fol))[1]))
            file_stacked = file_stacked.astype(np.float32)
            file = file.astype(np.float32)
            print(f"Stacking initial files from {fol}")
            file_stacked = np.dstack((file_stacked, file))
            trigger = False
        else:
            if idx >= os.listdir(os.path.join("Dataset", "done", fol)).__len__():
                break
            file = np.load(os.path.join("Dataset", "done", fol, os.listdir(os.path.join("Dataset", "done", fol))[idx]))
            file = file.astype(np.float32)
            file_stacked = np.dstack((file_stacked, file))
            print(f"Stacking {os.listdir(os.path.join('Dataset', 'done', fol))[idx]}")
            idx += 1
    np.save(os.path.join("Dataset", f"stacked_{fol}_data.npy"), file_stacked)

# import matplotlib.pyplot as p
# abp = np.load(os.path.join('Dataset', 'stacked_ABP_data.npy'))
# ppg = np.load(os.path.join('Dataset', 'stacked_PPG_data.npy'))
# abp_1 = np.load(os.path.join('Dataset', 'done', 'ABP', 'finalABPData_set_9.npy'))
# ppg_1 = np.load(os.path.join('Dataset', 'done', 'ABP', 'finalPPGData_set_9.npy'))




