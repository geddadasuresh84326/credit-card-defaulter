import numpy as np
import pandas as pd
import os,sys
from credit.exception import CreditException
from credit.logger import logging

from credit.entity.config_entity import ModelPusherConfig
from credit.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from sklearn.ensemble import RandomForestClassifier
import shutil

class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,
                 model_pusher_config:ModelPusherConfig):
        """
        Description: This is Model Pusher component
        =========================================================
        Params:
        model_evaluation_artifact: requires model_evaluation_artifact
        model_pusher_config  : requires model_pusher_config
        =========================================================
        """
        try:
            logging.info(f"{'>>'*10}  Model Pusher {'<<'*10}")

            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise CreditException(e,sys)
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        """
        Description: This function is used to initiate the model pusher component
        =========================================================
        Params:
        =========================================================
        returns  ModelPusherArtifact
        """
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path

            # Creating model pusher dir to save model
            logging.info(f"Saving model to model pusher dir")
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)

            # Saving model to Saved model dir
            logging.info(f"Saving model to Saved model dir")
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok= True)
            shutil.copy(src= trained_model_path,dst= saved_model_path)

            logging.info(f"{'>>'*10}  Model Pusher Completed{'<<'*10}")
            model_pusher_artifact = ModelPusherArtifact(model_file_path=trained_model_path,
                                                        saved_model_path=saved_model_path)
            return model_pusher_artifact

        except Exception as e:
            raise CreditException(e,sys)

    