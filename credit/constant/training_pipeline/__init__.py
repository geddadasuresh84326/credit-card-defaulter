import os

SAVED_MODEL_DIR = "saved_models"

"""
Training pipeline constants
"""
TARGET_COLUMN:str = "default.payment.next.month"
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

