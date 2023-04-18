import yaml
import sys
import os
import dill
import numpy as np
import pandas as pd
from concrete.constant import *
from concrete.exception import CustomException


def write_yaml_file(file_path: str, data: dict = None):
    """
    Create yaml file
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        raise CustomException(e, sys)


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    :param file_path: str location of file to save.
    :param array: numpy array data to save
    :return: save numpy array data to file
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) from e


def save_object(file_path: str, obj):
    """
    :param file_path: str
    :param obj: Any sort of object
    :return:
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)

        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_message = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema."
        if len(error_message) > 0:
            raise Exception(error_message)
        return dataframe

    except Exception as e:
        raise CustomException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    :param file_path: str location of file to load
    :return: numpy array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)
    except Exception as e:
        raise CustomException(e, sys) from e


def load_object(file_path: str):
    """
    file_path: str
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e
