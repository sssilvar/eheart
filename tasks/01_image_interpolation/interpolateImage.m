function [ interpolatedImage ] = interpolateImage(image, newShape, method)
% INTERPOLATEIMAGE  Reshape an image and interpolates it
%
%   interpolatedImage = interpolateImage(img, newShape, method) adds A to itself.

if nargin == 1
    newShape = [256, 256, 256];
    method = 'linear'
elseif nargin == 2
    method = 'linear'
end

% Get original size
[sx, sy, sz] = size(image);

rsx = sx / newShape(1);
rsy = sy / newShape(2);
rsz = sz / newShape(3);

fprintf('[  INFO  ] Original shape: %s\n', mat2str([sx, sy, sz]))
fprintf('[  INFO  ] New shape is going to be: %s\n', mat2str(newShape))
fprintf('[  INFO  ] Resample step: %s\n', mat2str([rsx, rsy, rsz]))

% Create an interpolator
[X,Y,Z] = ndgrid(rsx:rsx:sx, rsy:rsy:sy, rsz:rsz:sz);
interpolatedImage = interp3(image, X, Y, Z, method);

fprintf('[  OK  ] Output shape: %s\n\n', mat2str(size(interpolatedImage)))

end