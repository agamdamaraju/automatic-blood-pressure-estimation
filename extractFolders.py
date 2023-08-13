import os, shutil
import zipfile

os.chdir("G:")
print("Processing...")

cnt = 0
for fol in os.listdir(os.path.join('Dataset', 'zippedData')):
    with zipfile.ZipFile(os.path.join('Dataset', 'zippedData', fol), 'r') as zip_ref:
        zip_ref.extractall(os.path.join('Dataset', 'unzippedData'))
    cnt+=1
    print(f'Processed {fol}, count: {cnt}')
    # for subfol in os.listdir(os.path.join(os.path.join('finalData', 'new_data', fol))):
    #     shutil.copy(os.path.join('finalData', 'new_data', fol, subfol), os.path.join('finalData', 'folders'))