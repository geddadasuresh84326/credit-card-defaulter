import numpy as np
import pandas as pd
import os,sys

from credit.exception import CreditException
from credit.logger import logging
from credit.entity.config_entity import DataTransformationConfig
from credit.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        """
        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        logging.info(f"{'>>'*10} Data Transformation {'<<'*10}")
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise CreditException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info(f"inside read_data function")
            return pd.read_csv(file_path)
        except Exception as e:
            raise CreditException(e,sys)
        
    def rename_categories(self,dataframe:pd.DataFrame)->pd.DataFrame:
        try:
            logging.info(f"inside rename_categories function")

            replace_dict = {6:5,0:5}
            dataframe["EDUCATION"].replace(replace_dict,inplace= True)

            dataframe = dataframe.rename(columns={'PAY_0':'PAY_1','default.payment.next.month':'Default'})
            
            return dataframe
        except Exception as e:
            raise CreditException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            # Reading train and test dataframes 
            train_df = DataTransformation.read_data(file_path=self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(file_path=self.data_validation_artifact.valid_test_file_path)
            logging.info(f"{train_df.columns}")
            # Renaming categories and columns
            train_df = self.rename_categories(dataframe=train_df)
            test_df = self.rename_categories(dataframe=test_df)

            # Saving train and test dataframes
            transformed_trained_file_path = self.data_transformation_config.transformed_trained_file_path
            logging.info(f"{train_df.columns}")
            os.makedirs(os.path.dirname(transformed_trained_file_path),exist_ok=True)
            train_df.to_csv(transformed_trained_file_path,index=False,header=True)

            transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            os.makedirs(os.path.dirname(transformed_test_file_path),exist_ok=True)
            test_df.to_csv(transformed_test_file_path,index=False,header=True)

            # Preparing Data Transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_trained_file_path,transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path)
            
            logging.info(f"{'>>'*10} Data Transformation Completed{'<<'*10}")

            return data_transformation_artifact
        except Exception as e:
            raise CreditException(e,sys)
    
