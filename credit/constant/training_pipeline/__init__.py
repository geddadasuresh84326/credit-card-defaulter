import os

SAVED_MODEL_DIR = os.path.join("saved_models")

"""
Training pipeline constants
"""
TARGET_COLUMN:str = "Default"
PIPELINE_NAME:str = "Credit"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "UCI_Credit_Card.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

PROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
MODEL_FILE_NAME:str = "model.pkl"
SCHEMA_FILE_PATH:str = os.path.join("config","schema.yaml")
SCHEMA_DROP_COLS:str = "drop_cols"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDAITON_DIR_NAME:str = "data_validation"
DATA_VALIDAITON_VALID_DIR:str = "valid"
DATA_VALIDAITON_INVALID_DIR:str = "invalid"
DATA_VALIDAITON_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDAITON_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


"""
Model Trainer related constant start with MODE TRAINER VAR NAME
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.10

"""
Model Evaluation related constant start with MODE EVALUATION VAR NAME
"""
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME= "report.yaml"

"""
Model Pusher related constant start with MODE PUSHER VAR NAME
"""
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR