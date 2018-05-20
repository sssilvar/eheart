function [ output_args ] = registrateMostSimilar( train_mri, target_mri )
%REGISTRATEMOSTSIMILAR Register a volume from the training set to a target.
%   Then, applies the transformation matrix to its segmentation
%% Define Params
addpath('jsonlab-1.5', 'nii');
params = loadjson('params.json');
f = filesep;

%% Do the thing!
% Get subjects dirs
dir_train = fileparts(train_mri);
dir_target = fileparts(target_mri);

% 1. Apply the registration from the training to the target image
cmd = [params.elastix_path,  ' -f ', target_mri, ' -m ', train_mri,...
        ' -fMask ', train_mri, f, 'fixedMask.ext and/or']


end

