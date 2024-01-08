import yaml
from credit.exception import CreditException
from credit.logger import logging
import os,sys
import numpy as np
import dill
import pandas as pd
from credit.config import mongo_client
import pymongo
from imblearn.combine import SMOTETomek

def read_yaml_file(file_path:str)->dict:
    """
    Description: This function is used to read a yaml file
    =========================================================
    Params:
    file_path: path of the yaml file
    =========================================================
    return : dict
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CreditException(e,sys) from e 

def write_yaml_file(file_path: str,content: object,replace:bool=False)->None:
    """
    Description: This function is used to write a yaml file
    =========================================================
    Params:
    file_path: path of the yaml file
    content: data 
    replace: boolean 
    =========================================================
    return : None
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise CreditException(e,sys)
    
def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis= 1)
        logging.info(f"Row and columns in df: {df.shape}")

        return df
    except Exception as e:
        raise CreditException(e,sys)

def save_object(file_path:str,obj:object):
    """
    Description: This function is used to save an object
    =========================================================
    Params:
    file_path: path to which the object is to be stored
    obj: object to be stored
    =========================================================
    return : None
    """
    try:
        logging.info("Entered into save_object method of MainUtils")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited from save_object method of MainUtils")

    except Exception as e:
        raise CreditException(e,sys)

def load_object(file_path:str)->object:
    """
    Description: This function is used to load an object
    =========================================================
    Params:
    file_path: path from which the object is to be load
    =========================================================
    return : Object
    """
    try:
        logging.info("Entered into load_object method of MainUtils")
        if not os.path.exists(file_path):
            raise Exception(f"the file : {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)

        logging.info("Exited from load_object method of MainUtils")
    except Exception as e:
        raise CreditException(e,sys) from e 
    
def resample_data(df:pd.DataFrame)->pd.DataFrame:
    """
    Description: This function is used to resample the data
    =========================================================
    Params:
    df: pandas Dataframe to be resampled
    =========================================================
    return : Resampled pandas dataframe
    """
    try:
        logging.info("Inside resample_data method of mainutils")
        X = df.drop('default.payment.next.month',axis=1)
        y = df['default.payment.next.month']

        # Resampling the minority class. The strategy can be changed as required.
        smt = SMOTETomek(random_state=42,sampling_strategy='minority',n_jobs=-1)

        # Fit the model to generate the data.
        X_res, y_res = smt.fit_resample(X, y)

        return pd.concat([X_res,y_res],axis=1)
    except Exception as e:
        raise CreditException(e,sys) from e 
    
