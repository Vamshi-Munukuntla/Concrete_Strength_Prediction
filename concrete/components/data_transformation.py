import sys
import os

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, MinMaxScaler

from concrete.constant import *
from concrete.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from concrete.entity.config_entity import DataTransformationConfig
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.utils.utils import read_yaml_file, save_numpy_array_data, save_object, load_data
from warnings import filterwarnings
filterwarnings('ignore')


class DataTransformation:
    def __init__(self,
                 data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact
                 ):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            transform_columns = dataset_schema[TRANSFORM_COLUMN_KEY]

            logging.info('Transforming and Scaling on columns is started.')
            transform_pipeline = Pipeline(steps=[
                ('yeo-johnson', PowerTransformer(method='yeo-johnson', standardize=False)),
                ('scaler', MinMaxScaler())
            ])

            preprocessor = ColumnTransformer([
                ('transformer', transform_pipeline, transform_columns)
            ])

            logging.info('Columns are transformed and scaled.')

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys) from e

    def _remove_outliers_IQR(self, col, df):
        try:
            """
            We are capping the outliers by upper and lower limits
            """
            percentile25 = df[col].quantile(0.25)
            percentile75 = df[col].quantile(0.75)

            iqr = percentile75 - percentile25
            upper_limit = percentile75 + (1.5 * iqr)
            lower_limit = percentile25 - (1.5 * iqr)

            df.loc[(df[col] > upper_limit), col] = upper_limit
            df.loc[(df[col] < upper_limit), col] = lower_limit

            logging.info('Outliers are capped by upper and lower limits.')
            return df

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Obtaining training and test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info('Loading training and testing data as pandas dataframe.')

            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            numerical_columns = schema[NUMERICAL_COLUMN_KEY]

            for col in numerical_columns:
                self._remove_outliers_IQR(col=col, df=train_df)

            logging.info('Outliers are capped in train df')

            for col in numerical_columns:
                self._remove_outliers_IQR(col=col, df=test_df)

            logging.info("Outliers are capped in test df")

            logging.info("Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            print(input_feature_train_df)

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info('Applying preprocessing object on training dataframe and testing dataframe.')
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info('concatenating the train numpy array and target feature.')
            logging.info('concatenating the test numpy array and target feature.')

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info("Saving transformed training and testing array.")

            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info("Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message="Data Transformation is Successful",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )
            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Data Transformation log completed.{'<<' * 30} \n\n")
