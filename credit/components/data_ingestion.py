from credit.exception import CreditException
from credit.logger import logging
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from credit.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from credit.entity.artifact_entity import DataIngestionArtifact
from credit.constant.training_pipeline import FILE_NAME
from credit.utils.main_utils import get_collection_as_dataframe,resample_data

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*10} Data Ingestion {'<<'*10}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditException(e,sys) 

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        """
        Description: This function return collection as dataframe
        =========================================================
        Params:
        
        =========================================================
        return DataIngestionArtifact
        """
        try:
            logging.info(f"Exporting collection data as pandas dataframe")

            df:pd.DataFrame = get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )

            logging.info("Save data in feature store")

            # replace na with NaN
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            df = resample_data(df=df)

            # save data in feature store
            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            
            # Save df to feature store folder
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            # split dataset into train and test set
            logging.info("split dataset into train and test set")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            # create train and test directory folders if not available
            logging.info("create train and test directory folders if not available")
            train_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir,exist_ok=True)
            test_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(test_dir,exist_ok=True)

            # Save train and test dataframes
            logging.info("Save train and test dataframes")
            train_df.to_csv(path_or_buf = self.data_ingestion_config.training_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf = self.data_ingestion_config.testing_file_path,index=False,header=True)

            # Prepare artifact
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            logging.info(f"{'>>'*10}Data Ingestion Completed{'<<'*10}")
            return data_ingestion_artifact

        except Exception as e:
            raise CreditException(e,sys) 
    
