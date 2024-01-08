import numpy as np
import pandas as pd
import os,sys
from credit.exception import CreditException
from credit.logger import logging

from credit.entity.config_entity import ModelEvaluationConfig
from credit.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact,ModelEvaluationArtifact
from sklearn.ensemble import RandomForestClassifier

from credit.ml.metric.classification_metric import get_classfication_score
from credit.utils.main_utils import write_yaml_file,save_object,load_object
from credit.ml.model.estimator import ModelResolver
from credit.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                    model_trainer_artifact:ModelTrainerArtifact,
                    data_transformation_artifact:DataTransformationArtifact):
        """
        Description: This is Model Evaluation component
        =========================================================
        Params:
        model_evaluation_config: requires model_evaluation_config
        model_trainer_artifact  : requires model_trainer_artifact
        data_transformation_artifact  : requires data_transformation_artifact
        =========================================================
        """
        try:
            logging.info(f"{'>>'*10}  Model Evaluation {'<<'*10}")
            self.model_evaluation_config = model_evaluation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise CreditException(e,sys)


    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        """
        Description: This function is used to initiate the model evaluation
        =========================================================
        Params:
        =========================================================
        returns  ModelEvaluationArtifact
        """
        try:
            valid_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            valid_test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Reading valid train and test dataframes 
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df,test_df])
            
            x_df = df.drop("Default",axis = 1)
            y_true = df["Default"]

            trained_model_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()

            is_model_accepted = True
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    best_model_metric_artifact=None,
                    trained_model_path=trained_model_path,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact
                )
                logging.info(f"Model evaluation artifact : {model_evaluation_artifact}")

                return model_evaluation_artifact
            latest_model_file_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_file_path)
            trained_model = load_object(file_path=trained_model_path)

            y_trained_pred = trained_model.predict(x_df)
            y_latest_pred = latest_model.predict(x_df)

            trained_metric = get_classfication_score(y_pred=y_trained_pred,y_true=y_true)
            latest_metric = get_classfication_score(y_pred=y_latest_pred,y_true=y_true)

            improved_accuracy = trained_metric.f1_score - latest_metric.f1_score
            if self.model_evaluation_config.change_threshold < improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted = False

            
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_file_path,
                best_model_metric_artifact=latest_metric,
                trained_model_path=trained_model_path,
                train_model_metric_artifact=trained_metric
            )
            logging.info(f"Model Evaluation artifact : {model_evaluation_artifact}")

            model_eval_report = model_evaluation_artifact.__dict__
            # Saving report 
            write_yaml_file(file_path=self.model_evaluation_config.report_file_path,content=model_eval_report)
            logging.info(f"{'>>'*10}  Model Evaluation Completed{'<<'*10}")

            return model_evaluation_artifact

        except Exception as e:
            raise CreditException(e,sys)