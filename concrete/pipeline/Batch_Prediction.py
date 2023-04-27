from concrete.components.data_validation import Batch_Data_Validation
from concrete.config.configuration import Configuration
from concrete.logger import logging
from concrete.exception import CustomException
from concrete.constant import *
from concrete.utils.utils import load_object, read_yaml_file, save_data

import os
import sys
import pandas as pd
import numpy as np
import shutil


class Batch_Prediction:

    def __init__(self, config: Configuration = Configuration()):
        self.path = None
        self.folder = None
        logging.info(f"\n{'*' * 20} Batch Prediction Pipeline Initiated {'*' * 20}\n")

        # Getting data validation config info
        self.data_validation_config = config.get_data_validation_config()

        # Loading Model Pickle Object for Prediction
        self.model_obj = load_object(file_path=os.path.join(ROOT_DIR, PICKLE_FOLDER_NAME_KEY, 'model.pkl'))

        # Reading schema.yaml file to validate prediction files
        self.schema_file_path = self.data_validation_config.schema_file_path
        self.dataset_schema = read_yaml_file(file_path=self.schema_file_path)

    def initiate_bulk_prediction(self):
        """Function to predict from saved trained model for entire dataset.
        It returns the original dataset with concrete_compressive_strength column
        """
        try:
            logging.info(f"{'*' * 20} Bulk Prediction Model Selected {'*' * 20}")

            # Getting location of uploaded dataset
            self.folder = PREDICTION_DATA_SAVING_FOLDER_KEY
            self.path = os.path.join(self.folder, os.listdir(self.folder)[0])

            # Validating uploaded dataset
            logging.info(f"Validation log passed Dataset: [{self.path}]")
            pred_val = Batch_Data_Validation(self.path, self.data_validation_config)
            data_validation_status = pred_val.validate_dataset_schema()

            logging.info(f"Dataset for Prediction: [{self.path}]")

            if data_validation_status:
                # Reading uploaded .CSV file in pandas
                data_df = pd.read_csv(self.path)

                data_df.drop_duplicates(inplace=True)
                logging.info('Duplicated data values are dropped from the dataset.')

                # Predicting the Compressive Strength with the saved model object
                prediction = self.model_obj.predict(data_df)
                data_df['Compressive_Strength'] = prediction
                logging.info('Prediction from model done')

                logging.info("Saving prediction file for sending it to the user.")

                output_folder_file_path = os.path.join(ROOT_DIR, "Output Folder", CURRENT_TIME_STAMP, "Predicted.csv")
                if os.path.exists(os.path.join(ROOT_DIR, "Output Folder")):
                    shutil.rmtree(os.path.join(ROOT_DIR, "Output Folder"))

                save_data(file_path=output_folder_file_path, data=data_df)
                zipped_file = os.path.dirname(output_folder_file_path)

                shutil.make_archive(zipped_file, 'zip', zipped_file)
                shutil.rmtree(zipped_file)
                shutil.rmtree(self.folder)

                logging.info(f"{'*' * 20} Bulk Prediction Completed {'*' * 20}")
                return zipped_file + '.zip'

        except Exception as e:
            raise CustomException(e, sys) from e

