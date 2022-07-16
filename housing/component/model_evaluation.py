from housing.entity.model_factory import evaluate_regression_model
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import *
from housing.entity.artifact_entity import * 
from housing.util.util import *

import sys, os

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact) -> None:
        try:
            logging.info(f"{'=' * 30} Model Evaluation log started {'=' * 30}")
            self.model_evaluation_config = model_evaluation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path
            
            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(model_evaluation_file_path)
                return model
            model_evaluation_file_content = read_yaml_file(model_evaluation_file_path)
            model_evaluation_file_content = dict() if model_evaluation_file_content is None else model_evaluation_file_content
            
            if BEST_MODEL_KEY not in model_evaluation_file_content:
                return model
            
            model = load_object(file_path=model_evaluation_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]
            logging.info(f"Previous evaluation result is this {model_eval_content}")
            eval_result = {
                 BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,
                }
            }
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY:model_history}
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)
            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_content}")
            write_yaml_file(file_path=eval_file_path, data=model_eval_content) 
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def initate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            traind_model_obj = load_object(file_path=trained_model_file_path)
            
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(transformed_train_file_path)
            
            logging.info(f"Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            test_array = load_numpy_array_data(transformed_test_file_path)
            
            logging.info(f"Splitting Training And Testng input's input feature and output feature")
            X_train, y_train, X_test, y_test = train_array[:, :-1],  train_array[:, -1], test_array[:, :-1], test_array[:, -1]
            
            model = self.get_best_model()
            if model is None:
                logging.info(f"No previous model found . So accepthing the current model as best model")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True,
                                                                    evaluated_model_path=trained_model_file_path)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
                return model_evaluation_artifact
            model_list = [model, traind_model_obj]
            
            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                             X_train=X_train,
                                                             y_train=y_train,
                                                             X_test=X_test,
                                                             y_test=y_test,
                                                             base_accuracy=self.model_trainer_artifact.model_accuracy)
            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")
            
            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path)
                logging.info(response)
                return response
            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted= True,
                                                                    evaluated_model_path=trained_model_file_path)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model Accepted . Model evaluation artifact is this {model_evaluation_artifact}")
            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=False, 
                                                                    evaluated_model_path=trained_model_file_path)
            return model_evaluation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def __del__(self):
        logging.info(f"{'=' * 30} Model Evaluation log started {'=' * 30}")