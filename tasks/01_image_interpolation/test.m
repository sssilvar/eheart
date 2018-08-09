%% Add libraries
addpath(genpath('/home/sssilvar/Apps/vistasoft/fileFilters/nifti'));
close all

%% Load image an interpolate it
imgFile = '/home/sssilvar/Documents/data/eheart/patient001/patient001_frame01.nii.gz';
nii = niftiRead(imgFile)

[sx, sy, sz] = size(nii.data);

% Interpolate image
method = 'linear'
interpolatedImg = interpolateImage(double(nii.data), [sx, sy, 100], method);

[isx, isy, isz] = size(interpolatedImg);

% Return to original
reconstructedImg = interpolateImage(interpolatedImg, [sx, sy, sz], method);

%% Plot results
figure;

subplot(1,3,1) % slice 100
imshow(reshape(nii.data(:, 100, :), [sx, sz]), [])
title('Original');

subplot(1,3,2) % slice 160
imshow(reshape(interpolatedImg(:, 160, :), [isx, isz]), [])
title('Interpolated');

subplot(1,3,3) % slice 160
imshow(reshape(reconstructedImg(:, 128, :), [sx, sz]), [])
title('Interpolated');

% Figure
figure;

subplot(2,2,1)
imshow(nii.data(:,:,5), [])
title('Original')

subplot(2,2,2)
imshow(reconstructedImg(:,:,5), [])
title('Reconstructed from interpolation')

subplot(2,2,3)
imshow(reshape(nii.data(:,128,:), [sx, sz])', [])

subplot(2,2,4)
imshow(reshape(reconstructedImg(:,128,:), [sx, sz])', [])