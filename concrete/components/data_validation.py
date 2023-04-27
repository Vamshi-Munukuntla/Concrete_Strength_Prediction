import sys
import pandas as pd

from concrete.constant import *
from concrete.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from concrete.entity.config_entity import DataValidationConfig
from concrete.entity.raw_data_validation import IngestedDataValidation
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.utils.utils import read_yaml_file


class Batch_Data_Validation:
    def __init__(self, path, data_validation_config: DataValidationConfig):
        try:
            self.path = path
            self.data_validation_config = data_validation_config
            self.schema_file_path = self.data_validation_config.schema_file_path
            self.dataset_schema = read_yaml_file(file_path=self.schema_file_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    def file_name_check(self, file):
        try:
            file_check_status = False
            file_name = 'Concrete_Data.csv'
            if file == file_name:
                file_check_status = True
            else:
                raise Exception(f"File name is not as per the Schema in file: [{file}")

            return file_check_status
        except Exception as e:
            raise CustomException(e, sys) from e

    def column_check(self, file):
        try:
            data = pd.read_csv(file)

            # Finding number of columns in the dataset
            no_of_columns = data.shape[1]

            # Checking if the number of columns in dataset is as per defined schema
            if no_of_columns != self.dataset_schema['Number_of_Columns']:
                raise Exception(f"Number of columns is not correct in file: [{file}]")

            columns = list(data.columns)

            # Checking for column name, whether they are as per the defined schema
            for column in columns:
                if column not in self.dataset_schema["ColumnNames"].keys():
                    raise Exception(f"Column: [{column}] in file: [{file}] not available in the schema.")

            # Checking whether any column have entire rows as missing values
            count = 0
            col = []
            for column in columns:
                if len(data[column]) - data[column].count() == len(data[column]):
                    count += 1
                    col.append(column)
            if count > 0:
                raise Exception(f"Columns: [{col}] have entire row as missing value.")
            return True

        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_dataset_schema(self):
        try:
            logging.info("Validating the schema of the dataset")
            validation_status = False

            if self.file_name_check(os.path.basename(self.path)) and self.column_check(os.path.join(self.path)):
                validation_status = True

            logging.info('Schema Validation Completed')
            logging.info(f"Is dataset schema as per the defined schema? -> validation_status")
            return validation_status

        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        logging.info("Prediction Dataset Validation log complete")


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Validation log started.{'<<' * 30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_path = self.data_validation_config.schema_file_path
            self.train_data = IngestedDataValidation(
                validate_path=self.data_ingestion_artifact.train_file_path,
                schema_path=self.schema_path)
            self.test_data = IngestedDataValidation(
                validate_path=self.data_ingestion_artifact.test_file_path,
                schema_path=self.schema_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    def isFolderPathAvailable(self) -> bool:
        try:
            isfolder_available = False
            train_path = self.data_ingestion_artifact.train_file_path
            test_path = self.data_ingestion_artifact.test_file_path
            if os.path.exists(train_path):
                if os.path.exists(test_path):
                    isfolder_available = True
            return isfolder_available
        except Exception as e:
            raise CustomException(e, sys) from e

    def is_Validation_successful(self):
        try:
            validation_status = True
            logging.info("Validation Process Started")
            if self.isFolderPathAvailable():
                # Validating the train files
                logging.info("Validating the train files")
                train_filename = os.path.basename(
                    self.data_ingestion_artifact.train_file_path)

                is_train_filename_validated = self.train_data.validate_filename(
                    file_name=train_filename)

                is_train_column_numbers_validated = self.train_data.validate_column_length()

                is_train_column_name_same = self.train_data.check_column_names()

                is_train_missing_values_whole_column = self.train_data.missing_values_whole_column()

                self.train_data.replace_null_values_with_null()

                # Validating the test files
                logging.info("Validating the test files")
                test_filename = os.path.basename(
                    self.data_ingestion_artifact.test_file_path)

                is_test_filename_validated = self.test_data.validate_filename(
                    file_name=test_filename)

                is_test_column_numbers_validated = self.test_data.validate_column_length()

                is_test_column_name_same = self.test_data.check_column_names()

                is_test_missing_values_whole_column = self.test_data.missing_values_whole_column()

                self.test_data.replace_null_values_with_null()

                logging.info(
                    f"Train_set status|is Train filename validated?: {is_train_filename_validated}|is train columns "
                    f"validated?: {is_train_column_numbers_validated}|is train column name validated?: "
                    f"{is_train_column_name_same}|whole missing columns?{is_train_missing_values_whole_column}")
                logging.info(
                    f"Test_set status|is Test filename validated?: {is_test_filename_validated}is test col numbers "
                    f"validated?: {is_test_column_numbers_validated}|is test column names validated? "
                    f"{is_test_column_name_same}| whole missing columns? {is_test_missing_values_whole_column}")

                if is_train_filename_validated & is_train_column_numbers_validated & is_train_column_name_same & \
                        is_train_missing_values_whole_column:
                    pass
                else:
                    validation_status = False
                    logging.info("Check out Training Data! Validation Failed")
                    raise ValueError(
                        "Check your Training data! Validation failed")

                if is_test_filename_validated & is_test_column_numbers_validated & is_test_column_name_same & \
                        is_test_missing_values_whole_column:
                    pass
                else:
                    validation_status = False
                    logging.info("Check your Test data! Validation failed")
                    raise ValueError(
                        "Check your Testing data! Validation failed")

                logging.info("Validation Process Completed")
                return validation_status

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_validation(self):
        try:
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.schema_path,
                is_validated=self.is_Validation_successful(),
                message="Data Validation Performed"
            )
            logging.info(
                f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Data Validation log completed.{'<<' * 30}\n\n")
