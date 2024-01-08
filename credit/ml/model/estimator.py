from credit.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from credit.logger import logging
from credit.exception import CreditException
import os,sys


class ModelResolver:
    def __init__(self,model_dir:SAVED_MODEL_DIR=SAVED_MODEL_DIR):
        try:
            logging.info(f"Inside Model Resolver class")
            self.model_dir = model_dir
        except Exception as e:
            raise CreditException(e,sys)
    
    def get_best_model_path(self)->str:
        """
        Description: This function is used to get the best model path
        =========================================================
        Params:
    
        =========================================================
        return : path of the best model
        """
        try:
            logging.info(f"Inside get_best_model_path function to get latest model path")
            timestamps = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)

            return latest_model_path
        except Exception as e:
            raise CreditException(e,sys)

    def is_model_exists(self)->bool:
        """
        Description: This function is used to check whether the model is existed or not in a filepath
        =========================================================
        Params:
        
        =========================================================
        return : True/False
        """
        try:
            if not os.path.exists(self.model_dir):
                return False
            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False
            latest_model_path = self.get_best_model_path()
            if not os.path.exists(latest_model_path):
                return False
            return True
        except Exception as e:
            raise CreditException(e,sys)
