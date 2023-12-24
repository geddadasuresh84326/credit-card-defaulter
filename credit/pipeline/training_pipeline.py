from credit.exception import CreditException
from credit.logger import logging
import os,sys

from credit.entity.config_entity import TrainingPipelineConfig
from credit.entity.config_entity import DataIngestionConfig
from credit.entity.artifact_entity import DataIngestionArtifact
from credit.components.data_ingestion import DataIngestion


def start_training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()

        # Data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        # print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        raise CreditException(e,sys)