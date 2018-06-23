import os

import pandas as pd

current_dir = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # Set files an directories
    dataset_csv = os.path.join(current_dir, 'data_df.csv')

    dataset_folder = r"/run/media/ssilvari/HDD Data/Universidad/MSc/Thesis/Dataset/FreeSurferSD"
    out_folder = r"/run/media/ssilvari/HDD Data/Universidad/MSc/Thesis/Dataset/nifti"

    # Load CSV
    df = pd.read_csv(dataset_csv)

    # Start registering
    for subject in df['folder'][:2]:
        print('Registering subject: ', subject)

        out = os.path.join(out_folder, subject)

        try:
            print('Creating folder')
            os.mkdir(out)
        except FileExistsError:
            pass

        mgz = '"' + os.path.join(dataset_folder, subject, 'mri', 'brainmask.mgz') + '"'
        nii = '"' + os.path.join(out_folder, subject, 'brainmask.nii.gz') + '"'

        mgz_to_nii_cmd = 'mri_convert ' + mgz + ' ' + nii
        print(mgz_to_nii_cmd)
        os.system(mgz_to_nii_cmd)

        # Do same for masks
        mgz = '"' + os.path.join(dataset_folder, subject, 'mri', 'aseg.mgz') + '"'
        nii = '"' + os.path.join(out_folder, subject, 'aseg.nii.gz') + '"'

        mgz_to_nii_cmd = 'mri_convert ' + mgz + ' ' + nii
        print(mgz_to_nii_cmd)
        os.system(mgz_to_nii_cmd)
