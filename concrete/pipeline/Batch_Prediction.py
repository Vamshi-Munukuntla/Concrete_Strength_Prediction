from concrete.components.data_validation import DataValidation
from concrete.config.configuration import Configuration
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.constant import *
from concrete.utils.utils import load_object, read_yaml_file, save_data

import os
import sys
import shutil

import pandas as pd
import numpy as np


class Prediction:

    def __init__(self, config: Configuration = Configuration()):
        self.path = None
        self.folder = None
        logging.info(f"\n {'-' * 20} Prediction Pipeline Initiated {'-' * 20} \n")

        # Getting data validation config info
        self.data_validation_config = config.get_data_validation_config()

        # Loading Pickle Objects for prediction
        self.model_obj = load_object(file_path=os.path.join(ROOT_DIR, PICKLE_FOLDER_NAME_KEY, "model.pkl"))

        # Reading schema.yaml file to validate prediction data
        self.schema_file_path = self.data_validation_config.schema_file_path
        self.dataset_schema = read_yaml_file(file_path=self.schema_file_path)

    def initiate_bulk_prediction(self):
        """
        Function to predict from saved trained model for entire dataset.
        :return: returns the original dataset with prediction column.
        """

        try:
            logging.info(f"{'-' * 20}Bulk Prediction Mode Selected {'-' * 20}")

            # Getting location of uploaded dataset
            self.folder = PREDICTION_DATA_SAVING_FOLDER_KEY
            self.path = os.path.join(self.folder, os.listdir(self.folder)[0])

            # Validating uploaded dataset
            logging.info(f"Validating Passed dataset: [{self.path}]")
            pred_val = Prediction
        except Exception as e:
            raise CustomException(e, sys) from e

