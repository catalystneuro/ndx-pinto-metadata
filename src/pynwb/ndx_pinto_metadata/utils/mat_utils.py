import numpy as np
from scipy.io import loadmat
from scipy.io.matlab import mat_struct


def convert_mat_file_to_dict(file_path: str):
    """
    Convert ViRMEN output (.mat file) to a dictionary.

    Recursively converts all MATLAB objects to nested dictionaries.

    Parameters
    ----------
    file_path : str
            The path to .mat file containing the ViRMEN experiment metadata.
    """
    data = loadmat(file_path, struct_as_record=False, squeeze_me=True)
    for key in data:
        if isinstance(data[key], mat_struct):
            data[key] = _mat_obj_to_dict(data[key])
    return data


def _mat_obj_to_dict(mat: mat_struct) -> dict:
    """
    Recursive function to convert nested MATLAB struct objects to dictionaries.
    """
    dict_from_struct = {}
    for field_name in mat.__dict__["_fieldnames"]:
        dict_from_struct[field_name] = mat.__dict__[field_name]
        if isinstance(dict_from_struct[field_name], mat_struct):
            dict_from_struct[field_name] = _mat_obj_to_dict(
                dict_from_struct[field_name]
            )
        elif isinstance(dict_from_struct[field_name], np.ndarray):
            try:
                dict_from_struct[field_name] = _mat_obj_to_array(
                    dict_from_struct[field_name]
                )
            except TypeError:
                continue
    return dict_from_struct


def _mat_obj_to_array(mat_struct_array) -> np.array:
    """
    Constructs array from MATLAB cell arrays.
    """
    if any(isinstance(mat, mat_struct) for mat in mat_struct_array):
        array_from_cell = [_mat_obj_to_dict(mat_obj) for mat_obj in mat_struct_array]
        array_from_cell = np.array(array_from_cell)
    else:
        array_from_cell = mat_struct_array

    return array_from_cell
