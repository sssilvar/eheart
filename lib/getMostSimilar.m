function [ most_similar_image ] = getMostSimilar( target )
%GETMOSTSIMILAR Looks for the most similar image in a dataset
%   Based on the Normalized Cross Correlation metrix

clc % DELETE THIS LINE
%% Define params
addpath('jsonlab-1.5', 'nii');
params = loadjson('params.json');
f = filesep;
current_dir = fileparts(mfilename('fullpath'));

% Check if csv_data path is empty in json file
if isempty(params.csv_data)
    csv_data = [current_dir, f, 'dataset.csv'];
else
    csv_data = params.csv_data;
end

%% Start Processing!
% Load the target
mri_target = MRIread(target);

% Load the subjects' ID (folder names)
subjects = table2array(readtable(csv_data));

% Some indexes
c = 1;

for i = 1:length(subjects)
    % Define subject path
    subject_dir = [params.dataset_folder, f, subjects{i}];
    disp(['Processing subject: ', subjects{i}])
    
    % Get images inside folder: frames
    frames = getFramesfromFolderG2(subject_dir, 'frame', params.extension);
    for j = 1:length(frames)
        if ~any(strfind(frames{j}, 'gt')) % Avoid segmentation files
            file_vol = [subject_dir, f, frames{j}];
            
            % Read volume
            mri = MRIread(file_vol);
            ncc(c) = nccdecV(mri.vol, mri_target.vol);
            filenames{c} = file_vol;
        end
    end
    c = c + 1;
end

most_similar_image = filenames{find(ncc == max(ncc))};
fprintf('\n\n The most similar volume is:\n')
disp(most_similar_image)



