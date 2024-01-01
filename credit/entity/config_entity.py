from datetime import datetime
import os
from credit.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name:str = training_pipeline.PIPELINE_NAME
        self.artifact_dir:str = os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
        self.timestamp:str = timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name="creditcard"
        self.collection_name="customers"
        self.test_size = 0.2

        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.training_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path:str = os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME
        )

    
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDAITON_DIR_NAME)
        self.data_validation_valid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDAITON_VALID_DIR)
        self.data_validation_invalid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDAITON_INVALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.data_validation_valid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.data_validation_valid_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.data_validation_invalid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.data_validation_invalid_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(self.data_validation_dir,
                                                       training_pipeline.DATA_VALIDAITON_DRIFT_REPORT_DIR,
                                                       training_pipeline.DATA_VALIDAITON_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_trained_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.transformed_test_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TEST_FILE_NAME)
        self.transformed_object_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,training_pipeline.PROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path:str = os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_accuracy:float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold:float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir:str= os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold:float = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_PUSHER_DIR_NAME)
        self.model_file_path:str = os.path.join(self.model_pusher_dir,training_pipeline.MODEL_FILE_NAME)

        timestamp = round(datetime.now().timestamp())

        self.saved_model_path:str = os.path.join(training_pipeline.SAVED_MODEL_DIR,f"{timestamp}",training_pipeline.MODEL_FILE_NAME)


