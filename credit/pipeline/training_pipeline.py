from credit.exception import CreditException
from credit.logger import logging
import os,sys

from credit.entity.config_entity import TrainingPipelineConfig
from credit.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from credit.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from credit.components.data_ingestion import DataIngestion
from credit.components.data_validation import DataValidation
from credit.components.data_trasformation import DataTransformation
from credit.components.model_trainer import ModelTrainer
from credit.components.model_evaluation import ModelEvaluation
from credit.components.model_pusher import ModelPusher

def start_training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()

        # Data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        # print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,                               data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()

        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                           model_trainer_artifact=model_trainer_artifact,
                                           data_transformation_artifact=data_transformation_artifact)
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

        model_pusher_config = ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                   model_evaluation_artifact=model_evaluation_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
        
    except Exception as e:
        raise CreditException(e,sys)