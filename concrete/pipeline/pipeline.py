import sys

from concrete.components.data_ingestion import DataIngestion
# from concrete.components.data_validation import DataValidation
from concrete.config.configuration import Configuration
from concrete.entity.artifact_entity import DataIngestionArtifact
# from concrete.entity.artifact_entity import DataValidationArtifact
from concrete.exception import CustomException


class Pipeline:

    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise CustomException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            # data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e, sys) from e
