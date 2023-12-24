from credit.exception import CreditException
from credit.logger import logging
import os,sys

from credit.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from credit.entity.config_entity import TrainingPipelineConfig,DataValidationConfig
from credit.constant.training_pipeline import SCHEMA_FILE_PATH
from credit.utils.main_utils import read_yaml_file,write_yaml_file

import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            logging.info(f"{'>>'*10} Data Validation {'<<'*10}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CreditException(e,sys)
        
    def drop_zero_std_columns(self,dataframe):...

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f" Required number of columns : {number_of_columns}")
            logging.info(f" Data frame has columns : {len(dataframe.columns)}")
            if number_of_columns == len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise CreditException(e,sys)

    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_columns.append(num_column)
            logging.info(f" Missing numerical columns :[{missing_numerical_columns}]")
            return numerical_column_present
        
        except Exception as e:
            raise CreditException(e,sys)
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CreditException(e,sys)
    
    def detect_data_drift(self,base_df,current_df,threshold = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})

                drift_report_file_path = 
        except Exception as e:
            raise CreditException(e,sys)

