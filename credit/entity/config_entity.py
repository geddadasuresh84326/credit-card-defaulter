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
        