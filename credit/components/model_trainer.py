import numpy as np
import pandas as pd
import os,sys
from credit.exception import CreditException
from credit.logger import logging

from credit.entity.config_entity import ModelTrainerConfig
from credit.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from sklearn.ensemble import RandomForestClassifier

from credit.ml.metric.classification_metric import get_classfication_score
from credit.utils.main_utils import save_object

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                        data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*10}  Model Training {'<<'*10}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CreditException(e,sys)
    
    def train_model(self,x_train,y_train):
        try:
            logging.info(f"Inside train model function")
            rfc_clf = RandomForestClassifier(n_estimators=20,oob_score=True,n_jobs=1,random_state=42,max_features=None,min_samples_leaf=10)
            rfc_clf.fit(x_train,y_train)

            return rfc_clf
        except Exception as e:
            raise CreditException(e,sys)

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info(f"Getting trasformed train and test data filepaths")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            logging.info(f"Reading train and test data")
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            logging.info(f"Seperating input and target features of train and test data")
            x_train = train_df.drop("Default",axis=1)
            y_train = train_df["Default"]

            x_test = test_df.drop("Default",axis=1)
            y_test = test_df["Default"]

            logging.info(f"Training  the model")
            rfc_clf = self.train_model(x_train,y_train)

            logging.info(f"Getting predictions and calculating performance scores")
            y_train_pred = rfc_clf.predict(x_train)
            y_test_pred = rfc_clf.predict(x_test)

            classification_train_metric = get_classfication_score(y_true=y_train,y_pred=y_train_pred)
            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Model is not providing expected accuracy")
            logging.info(f"Classification train metric : {classification_train_metric}")

            classification_test_metric = get_classfication_score(y_true=y_test,y_pred=y_test_pred)
            logging.info(f"Classification test metric : {classification_test_metric}")

            # overfitting and underfitting
            # logging.info(f"Checking overfitting and underfitting conditions")
            # diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            # if diff > self.model_trainer_config.overfitting_underfitting_threshold:
            #     raise Exception("Model is overfitted or underfitted try to do more experiments")
            
            # Saving model
            logging.info(f"Saving the model")
            model_dir_path = self.model_trainer_config.trained_model_file_path
            os.makedirs(os.path.dirname(model_dir_path),exist_ok = True)
            
            save_object(file_path=model_dir_path,obj=rfc_clf)

            # Preparing model_trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=model_dir_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info(f"{'>>'*10} Model Training Completed{'<<'*10}")
            return model_trainer_artifact

        except Exception as e:
            raise CreditException(e,sys)