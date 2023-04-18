import sys

import numpy as np
from concrete.constant import *
from concrete.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from concrete.entity.config_entity import DataTransformationConfig
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.utils.utils import read_yaml_file


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

