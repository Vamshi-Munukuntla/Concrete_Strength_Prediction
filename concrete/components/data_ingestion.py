import os
import sys
from six.moves import urllib
import numpy as np
import pandas as pd
from concrete.constant import *
from concrete.logger import logging
from concrete.entity.config_entity import DataIngestionConfig
from concrete.entity.artifact_entity import DataIngestionArtifact
from concrete.config.configuration import Configuration
from concrete.exception import CustomException
from concrete.utils.utils import read_yaml_file  # helper function
from sklearn.model_selection import train_test_split
from datetime import date


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>' * 30}Data Ingestion log started.{'<<' * 30} \n\n")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise CustomException(e, sys) from e

    def download_data(self) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok=True)

            concrete_strength_file_name = os.path.basename(download_url)

            raw_file_path = os.path.join(raw_data_dir, concrete_strength_file_name)

            logging.info(
                f"Downloading file from :[{download_url}] into :[{raw_file_path}]")
            urllib.request.urlretrieve(download_url, raw_file_path)
            logging.info(
                f"File :[{raw_file_path}] has been downloaded successfully.")
            return raw_file_path

        except Exception as e:
            raise CustomException(e, sys) from e

    def split_data_as_train_and_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            concrete_strength_file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Reading csv file: [{concrete_strength_file_path}]")

            # creating the date object of today's date
            today_date = date.today()
            current_year = today_date.year

            us_visa_dataframe = pd.read_csv(concrete_strength_file_path)

            logging.info(f"Splitting data into train and test")

            train_set = None
            test_set = None

            train_set, test_set = train_test_split(us_visa_dataframe, test_size=0.2, random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                           file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                          file_name)
            # ***********************************************************************************************
            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path, index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data Ingestion completed successfully."
                                                            )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            logging.info(f"Data Ingestion is completed \n\n")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            self.download_data()
            return self.split_data_as_train_and_test()
        except Exception as e:
            raise CustomException(e, sys) from e

