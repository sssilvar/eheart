import os

import pandas as pd

current_dir = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # Set files an directories
    dataset_csv = os.path.join(current_dir, 'data_df.csv')
    mni_folder = os.path.join(current_dir, 'fsaverage')

    dataset_folder = r'/data'

    out_folder = '/output'

    # Load CSV
    df = pd.read_csv(dataset_csv)

    # Template files
    fixed = os.path.join(mni_folder, 'brainmask.nii.gz')
    f_mask = os.path.join(mni_folder, 'aseg.nii.gz')

    # Start registering
    for subject in df['folder'][:2]:
        print('Registering subject: ', subject)

        move = os.path.join(dataset_folder, subject, 'brainmask.nii.gz')
        m_mask = os.path.join(dataset_folder, subject, 'aseg.nii.gz')

        out = os.path.join(out_folder, subject)

        try:
            print('Creating folder')
            os.mkdir(out)
        except FileExistsError:
            pass

        registration_command = 'elastix -f ' + fixed + ' ' \
                               '-m ' + move + ' ' \
                               '-out ' + out + ' ' \
                               '-p /root/params/Par0018_3D_rigid_MI.txt ' \
            # '-fMask ' + f_mask + ' ' \
                               # '-mMask ' + m_mask + ' ' \
                               # '-p /root/params/Par0018_3D_rigid_MI.txt ' \
                               # '-p /root/params/Par0018_3D_bspline_MI_15.txt '  # '-p /root/params/Par0018_3D_affine_MI.txt ' \

        print(registration_command)
        os.system(registration_command)
