from concrete.pipeline.pipeline import Pipeline
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.config.configuration import Configuration
from concrete.components.data_ingestion import DataIngestion
import os


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")


if __name__ == "__main__":
    main()
