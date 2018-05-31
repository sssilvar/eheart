import os

import numpy as np
import pandas as pd
import nibabel as nb
# import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_dilation
from scipy.ndimage import interpolation

# plt.style.use('ggplot')

from lib import get_files_by_ext_and_pat


def dilate_roi(data_folder, dataset_csv, roi_val):
    # Load dataset
    df = pd.read_csv(dataset_csv)

    # Iterate over the subjects
    for subject in df['sid']:
        subject_dir = os.path.join(data_folder, subject)

        gt_images = get_files_by_ext_and_pat(folder=subject_dir, ext=ext, pat=gt_pat)
        mr_images = [el.replace(gt_pat, '') for el in gt_images]

        print('[  INFO  ] Subject ', subject, ' has the following images assosiated')
        print('\tGround truth:\n\t', gt_images)
        print('\tMRIs:\n\t', mr_images)

        if len(gt_images) > 1 and len(mr_images) > 1:
            for gt_image in gt_images:
                # load image
                nii_gt = nb.load(os.path.join(subject_dir, gt_image))
                vol_gt = (nii_gt.get_data() == roi_val).astype(np.uint8)

                # Dilate image
                vol_dilated = binary_dilation(vol_gt, iterations=12).astype(nii_gt.get_data_dtype())

                # Save it
                file_dilated = os.path.join(subject_dir, gt_image.replace(gt_pat, '_dilated'))
                nii_dilated = nb.Nifti1Image(vol_dilated, nii_gt.get_affine())
                nb.save(nii_dilated, file_dilated)
                os.chmod(file_dilated, 766)

            else:
                print('[  WARNING  ] There is just one frame for subject: ' + subject)


def normalized_cross_correlation_vol(vol_a, vol_b):
    # Cast to np.array
    vol_a = np.array(vol_a)
    vol_b = np.array(vol_b)

    # Preprocess them
    dsfactor = [w / float(f) for w, f in zip(vol_a.shape, vol_b.shape)]
    vol_b = interpolation.zoom(vol_b, zoom=dsfactor)

    # Define some conditions
    l = vol_a.shape
    f = [i == j for i, j in zip(vol_a.shape, vol_b.shape)]

    print('\tA - Shape: ', vol_a.shape)
    print('\tB - Shape: ', vol_b.shape)
    print('\tShape comparison: ', f)

    # Check dimensionality compatibility
    if np.sum(f) == len(l):
        print('\n[  INFO  ] Calculating Normalized cross-correlation...')
        posA = np.where(vol_a != 0)
        posB = np.where(vol_b != 0)

        a_loc = vol_a[posA]
        b_loc = vol_a[posB]

        meA = np.mean(a_loc)
        meB = np.mean(b_loc)

        a_dot = (a_loc - meA)  # / np.linalg.norm((a_loc - meA))
        b_dot = (b_loc - meB)  # / np.linalg.norm((b_loc - meB))

        try:
            ncc = np.mean(a_dot * b_dot) * 100
        except ValueError as e:
            print(e)
            ncc = 0

        return ncc
    else:
        print('[  WARNING  ] Volumes are different size')
        return 0


def find_most_similar(data_folder, csv_file, target_file):
    # Load dataset
    df = pd.read_csv(csv_file)

    # Load target volume
    nii_target = nb.load(target_file)
    vol_target = nii_target.get_data()

    # Iterate over the subjects
    for subject in df['sid']:
        subject_dir = os.path.join(data_folder, subject)

        gt_images = get_files_by_ext_and_pat(folder=subject_dir, ext=ext, pat=gt_pat)
        mr_images = [el.replace(gt_pat, '') for el in gt_images]

        if len(gt_images) > 1 and len(mr_images) > 1:
            for mr_image in mr_images:
                print(' Comparing with: ' + mr_image)

                # Load MRI
                mr_filename = os.path.join(subject_dir, mr_image)
                nii_mr = nb.load(mr_filename)
                vol_mr = nii_mr.get_data()

                print('\tNCC: ', normalized_cross_correlation_vol(vol_target, vol_mr))
            else:
                print('[  WARNING  ] There is just one frame for subject: ' + subject)


def dataset_to_template(data_folder, out_folder, csv_file, template_file):
    # Load dataset
    df = pd.read_csv(csv_file)

    # Iterate over the subjects
    for subject in [df['sid'][0]]:
        subject_dir = os.path.join(data_folder, subject)

        gt_images = get_files_by_ext_and_pat(folder=subject_dir, ext=ext, pat=gt_pat)
        mr_images = [el.replace(gt_pat, '') for el in gt_images]

        if len(gt_images) > 1 and len(mr_images) > 1:
            for mr_image in mr_images:
                subj_out_folder = os.path.join(out_folder, subject)

                # Create a folder (if necessary)
                try:
                    os.mkdir(subj_out_folder)
                except Exception as e:
                    pass

                # Registration command
                cmd = 'elastix -f ' + template_file + \
                      ' -m ' + mr_image + \
                      ' -p /root/params/parameters3.txt' + \
                      ' -out ' + subj_out_folder
                print(cmd)
                os.system(cmd)


        else:
            print('[  WARNING  ] There is just one frame for subject: ' + subject)


if __name__ == '__main__':
    # Set variable names
    csv_file = '/py/dataset.csv'

    data_folder = '/data'
    output_folder = '/output'
    ext = '.nii.gz'
    gt_pat = '_gt'
    end_val = 3  # Value for the endocardium

    target = '/data/patient001/patient001_frame01.nii.gz'
    template_file = '/data/template/template_ED.nii.gz'

    # find_most_similar(data_folder=data_folder, csv_file=csv_file, target_file=target)
    dataset_to_template(data_folder=data_folder,
                        out_folder=os.path.join(output_folder, 'processed'),
                        csv_file=csv_file,
                        template_file=template_file)

    # Register
    cmd = 'elastix -f /data/patient001/patient001_frame01.nii.gz ' \
          '-m /data/patient003/patient003_frame01.nii.gz ' \
          '-fMask /data/patient001/patient001_frame01_gt.nii.gz ' \
          '-mMask /data/patient003/patient003_frame01_gt.nii.gz ' \
          '-out /output/patient001_003 ' \
          '-p /root/params/Par0018_3D_rigid_MI.txt ' \
          '-p /root/params/Par0018_3D_affine_MI.txt ' \
          '-p /root/params/Par0018_3D_bspline_MI_15.txt ' \
 \
        # print('\n\n[  INFO  ] looking for ground truth files')
    # files = get_file_list_by_ext(data_folder, ext)
    # files = get_pattern_from_list(files, gt_pat)
    #
    # print('\n\n[  INFO  ] Extracting endocardium')
    # subject_file = '/data/patient001/patient001_frame01.nii.gz'
    # gt_file = '/data/patient001/patient001_frame01_gt.nii.gz'
    #
    # nii = nb.load(subject_file)
    # img = nii.get_data()
    # end_vol = (img == end_val).astype(np.int)
    #
    # # st = generate_binary_structure(3, 1)
    # end_dil = binary_dilation(end_vol, iterations=15)
    #
    # # Loading original image
    # nii = nb.load(gt_file)
    # img = nii.get_data()
    #
    # # end_vol = end_vol * img
    # # end_dil = end_dil * img
    #
    # # slice = 5
    # # plt.subplot(1,2,1)
    # # plt.imshow(end_vol[:, :, slice], cmap='gray')
    # # plt.subplot(1, 2, 2)
    # # plt.imshow(end_dil[:, :, slice], cmap='gray')
    # # plt.show()
    #
    # new_nii = nb.Nifti1Image(end_dil.astype(np.uint8), np.eye(4))
    # nb.save(new_nii, os.path.join(output_folder, 'test_mask.nii.gz'))
    #
    # cmd = 'elastix -f /data/patient001/patient001_frame01.nii.gz ' \
    #       '-m /data/patient003/patient003_frame01.nii.gz ' \
    #       '-fMask /data/patient001/patient001_frame01_gt.nii.gz ' \
    #       '-mMask /data/patient003/patient003_frame01_gt.nii.gz ' \
    #       '-out /output/patient001_003 ' \
    #       '-p /root/params/Par0018_3D_rigid_MI.txt ' \
    #       '-p /root/params/Par0018_3D_affine_MI.txt ' \
    #       '-p /root/params/Par0018_3D_bspline_MI_15.txt ' \
    #
    # print('\n\n[  INFO  ] Running registration')
    # print(cmd)
    # os.system(cmd)
