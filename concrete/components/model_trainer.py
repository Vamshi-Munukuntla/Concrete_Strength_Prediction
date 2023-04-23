import os
import sys
from typing import List

from concrete.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from concrete.entity.config_entity import ModelTrainerConfig
from concrete.entity.model_factory import MetricInfoArtifact, ModelFactory, GridSearchedBestModel
from concrete.entity.model_factory import evaluate_regression_model
from concrete.exception import CustomException
from concrete.logger import logging
from concrete.utils.utils import load_numpy_array_data, save_object, load_object


class ConcreteStrengthPredictor:
    def __init__(self, preprocessing_object, trained_model_object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):

        try:
            logging.info(f"{'>>' * 30} Model trainer log started.{'<<' * 30}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training dataset.")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            logging.info("Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            logging.info("Splitting training and testing input and target feature")
            X_train, y_train, X_test, y_test = train_array[:, :-1], train_array[:, -1],\
                test_array[:, :-1], test_array[:, -1]

            logging.info("Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)

            base_r2_score = self.model_trainer_config.base_r2_score
            logging.info(f"Expected r2 score: {base_r2_score}")

            logging.info("Initiating operation model selection")
            best_model = model_factory.get_best_model(X=X_train, y=y_train, base_r2_score=base_r2_score)

            logging.info(f"Best model found on training dataset: {best_model}")

            logging.info("Extracting trained model list.")
            grid_searched_best_model_list: List[GridSearchedBestModel] = model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list]
            logging.info("Evaluated all trained models on training and testing datasets.")
            metric_info: MetricInfoArtifact = evaluate_regression_model(model_list=model_list,
                                                                        X_train=X_train,
                                                                        y_train=y_train,
                                                                        X_test=X_test,
                                                                        y_test=y_test,
                                                                        base_r2_score=base_r2_score)
            print(metric_info)
            print(metric_info.model_name)
            logging.info(f"Best found model on both training and testing dataset.")

            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object

            trained_model_file_path = self.model_trainer_config.trained_model_file_path

            concrete_model = ConcreteStrengthPredictor(preprocessing_object=preprocessing_obj,
                                                       trained_model_object=model_object)

            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path, obj=concrete_model)

            model_trainer_artifact = ModelTrainerArtifact(is_trained=True,
                                                          message="Model Trained Successfully",
                                                          trained_model_file_path=trained_model_file_path,
                                                          train_r2_score=metric_info.train_r2_score,
                                                          test_r2_score=metric_info.test_r2_score,
                                                          rmse=metric_info.RMSE)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30} Model trainer log completed. {'<<'*30}")
