import os

import numpy as np
from scipy.ndimage.measurements import center_of_mass


def get_file_list_by_ext(folder, ext):
    """
    :param path: Dataset path
    :param ext: Extension to be found
    :return: List of files in that directory
    """
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                file_found = os.path.join(root, file)
                file_list.append(file_found)

    return file_list


def get_pattern_from_list(str_list, pattern):
    """
    Looks for a string pattern in a String list element.
    :param str_list: A list of strings
    :param pattern: str. A string pattern to be extracted
    :return: A list of strings that contains the pattern
    """
    filtererd_list = []
    for elm in str_list:
        if pattern in elm:
            filtererd_list.append(elm)

    return filtererd_list


def get_files_by_ext_and_pat(folder, ext, pat):
    files = get_file_list_by_ext(folder, ext)
    files_filtered = get_pattern_from_list(files, pat)

    return files_filtered


def get_centroid(mat):
    """
    Gets the center of mass coordinates of a n-dimensional matrix
    :param mat: nd-array
    :return: tuple, or list of tuples.
        Coordinates of centers-of-mass.
    """
    centroid_coordinates = np.ceil(center_of_mass(mat)).astype(np.int)
    return centroid_coordinates
