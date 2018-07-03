import os, time

import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Set start time
    ti = time.time()

    # Set files
    main_folder = '/user/ssilvari/home/Downloads/test'

    fixed_img = sitk.ReadImage(os.path.join(main_folder, 'msm_us.nii'))
    mobile_img = sitk.ReadImage(os.path.join(main_folder, 'msm_mri4.nii'))
    fixed_mask = sitk.ReadImage(os.path.join(main_folder, 'mask_us.nii'))
    mobile_mask = sitk.ReadImage(os.path.join(main_folder, 'mask_mri3.nii'))

    fixed_mask.SetDirection(fixed_img.GetDirection())
    mobile_mask.SetOrigin(mobile_img.GetOrigin())

    # print('\n\nRegistration info:')
    # print('\t\t- Fixed image: ' + fixed_img)
    # print('\t\t- Mobile image: ' + mobile_img)

    parameterMap = sitk.GetDefaultParameterMap("affine")
    parameterMap["AutomaticScalesEstimation"] = ["true"]
    parameterMap["AutomaticTransformInitialization"] = ["true"]
    parameterMap["Scales"] = ["float"]
    parameterMap["MaximumNumberOfSamplingAttempts"] = ["10"]
    parameterMap["FixedImagePyramid"] = ["FixedShrinkingImagePyramid"] 
    parameterMap["MovingImagePyramid"] = ["MovingShrinkingImagePyramid"]

    gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
    gaussian.SetSigma ( 1.5 )
    smoothed_mask = gaussian.Execute( sitk.Cast(fixed_mask, sitk.sitkUInt8) )

    binarizer = sitk.BinaryThresholdImageFilter()
    binarizer.SetLowerThreshold(0.1)
    smoothed_mask =  binarizer.Execute(smoothed_mask)
    sitk.WriteImage(smoothed_mask, 'smoothed.nii.gz')

    # Reshape Moving image
    output_spacing = fixed_img.GetSpacing()
    output_direction = fixed_img.GetDirection()
    output_origin = mobile_img.GetOrigin()
    output_size = fixed_img.GetSize()

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed_img)
    resampler.SetTransform(sitk.Transform())

    m_img_rs = resampler.Execute(mobile_img)
    m_msk_rs = resampler.Execute(mobile_mask)

    sitk.WriteImage(m_msk_rs, 'resized.nii.gz')

    print(np.sum(sitk.GetArrayFromImage(fixed_mask)))
    
    # Setup pipeline for registration
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.LogToConsoleOn()
    elastixImageFilter.SetFixedImage(fixed_img)
    elastixImageFilter.SetMovingImage(mobile_img)
    elastixImageFilter.SetFixedMask(sitk.Cast(smoothed_mask, sitk.sitkUInt8))
    elastixImageFilter.SetMovingMask(sitk.Cast(mobile_mask, sitk.sitkUInt8))


    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.Execute()
    sitk.WriteImage(elastixImageFilter.GetResultImage(), 'registered.nii.gz')

    # Check execution time
    tf = time.time()
    print('Total task %f' % (tf - ti))
