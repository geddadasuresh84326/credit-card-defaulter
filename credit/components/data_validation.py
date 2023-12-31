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
        """
        Description: This is Data Validation component
        =========================================================
        Params:
        data_ingestion_artifact: requires data_ingestion_artifact
        data_validation_config  : requires data_validation_config
        =========================================================
        """
        try:
            logging.info(f"{'>>'*10} Data Validation {'<<'*10}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CreditException(e,sys)
        
    def drop_zero_std_columns(self,dataframe):...

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        """
        Description: This function is used to validate the number of columns in a dataframe
        =========================================================
        Params:
        file_path: requires Dataframe
        =========================================================
        returns True/False
        """
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
        """
        Description: This function is used to check the numerical columns existed or not
        =========================================================
        Params:
        file_path: requires Dataframe
        =========================================================
        returns True/False
        """
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
        """
        Description: This function is used to read the data
        =========================================================
        Params:
        file_path: requires the path of data
        =========================================================
        returns pandas dataframe
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CreditException(e,sys)
    
    def detect_data_drift(self,base_df,current_df,threshold = 0.05)->bool:
        """
        Description: This function is used to find the datadrift
        =========================================================
        Params:
        file_path: requires Dataframe
        =========================================================
        returns True/False
        """
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

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path),exist_ok= True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise CreditException(e,sys)


    def initiate_data_validation(self)-> DataValidationArtifact:
        """
        Description: This function is used to initiate the data validation
        =========================================================
        Params:
        =========================================================
        returns  DataValidationArtifact
        """
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read train and test dataframes
            logging.info(f"Reading data from train and test locations started")
            train_dataframe = DataValidation.read_data(file_path = train_file_path)
            test_dataframe = DataValidation.read_data(file_path=test_file_path)

            # Validate columns
            logging.info(f" validation of number of columns started")
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} train dataframe does not contain all the columns. \n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} test dataframe does not contain all the columns. \n"
            
            # Validate numerical columns
            logging.info(f" validation of numerical columns started")
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} train dataframe does not contain all numerical columns. \n"
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} test dataframe does not contain all numerical columns. \n"
            
            # lets check data drift
            status = self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            logging.info(f"{'>>'*10} Data Validation Completed{'<<'*10}")

            return data_validation_artifact
        except Exception as e:
            raise CreditException(e,sys)