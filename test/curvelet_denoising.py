from __future__ import print_function

import os

import pyct as ct
import numpy as np
import nibabel as nb

import matplotlib.pyplot as plt

def select_scale(fdct, f, th):
    # Print Information
    for scale in range(0, fdct.nbs):
        if scale == 0:
            angles = [0]
        elif scale == 1:
            angles = range(0, fdct.nba)
        elif scale % 2 == 0:
            angles = range(0, int(scale * fdct.nba))
        elif scale % 2 != 0:
            angles = range(0, int((scale - 1) * fdct.nba))
        else:
            angles = []
            raise ValueError('There is no angles inside the scale')

        # Go over all the angles in the scale
        for angle in angles:
            if scale not in th:
                ix = fdct.index(scale)
                # Delete data for testing
                f[ix[0]:ix[1]] = 0
    return f

if __name__ == '__main__':
    # Params
    n_scales = 10
    n_angles = 16
    scale_selected = [0, 1, 2, 3, 4, 7, 8]
    nii_file = '/user/ssilvari/home/code/eheart/data/patient004/patient004_frame15.nii.gz'
    nii_gt = '/user/ssilvari/home/code/eheart/data/patient004/patient004_frame15_gt.nii.gz'

    # Load image
    nii = nb.load(nii_file).get_data()
    mask = nb.load(nii_gt).get_data()
    nii = nii * mask

    # Select a slide (2D)
    slice_ix = nii.shape[2] // 2
    img = nii[:, :, slice_ix].astype(np.float).T
    img = (img / img.max()) * 256

    # Setup curvelet params
    A = ct.fdct2(img.shape, nbs=n_scales, nba=n_angles, ac=True, norm=False, vec=True, cpx=False)

    # Apply curvelet to the image and select one scale
    f = A.fwd(img)
    f = select_scale(A, f, scale_selected)

    # Reconstruct the image
    y = A.inv(f) * mask[:,:, slice_ix].T

    fig, ax = plt.subplots(1, 2, sharey='all')
    ax[0].imshow(img, cmap='viridis')
    ax[0].set_title('Original')

    ax[1].imshow(np.abs(y), cmap='viridis')
    ax[1].set_title('Reconstructed (Only scale(s) %s)' % str(scale_selected))
    # plt.savefig(os.path.join('/home/sssilvar/Documents/output/', 'scale_%d_removed.png' % s), bbox_inches='tight')
    plt.show()
    


