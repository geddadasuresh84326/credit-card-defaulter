import numpy as np
from flask import Flask, request, jsonify, render_template
from bson.objectid import ObjectId
import pickle
from credit.logger import logging
from credit.utils.main_utils import load_object
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():

    """Get the user input from the form """
    Gender = request.form["gender"]
    Education = request.form["education"]
    Marital_status = request.form["marriage"]
    Age = request.form["age"]
    Limit_balance = request.form["limit_bal"]
    PAY_1 = request.form["pay_1"]
    PAY_2 = request.form["pay_2"]
    PAY_3 = request.form["pay_3"]
    PAY_4 = request.form["pay_4"]
    PAY_5 = request.form["pay_5"]
    PAY_6 = request.form["pay_6"]
    BILL_AMT1 = request.form["bill_amt1"]
    BILL_AMT2 = request.form["bill_amt2"]
    BILL_AMT3 = request.form["bill_amt3"]
    BILL_AMT4 = request.form["bill_amt4"]
    BILL_AMT5 = request.form["bill_amt5"]
    BILL_AMT6 = request.form["bill_amt6"]
    PAY_AMT1 = request.form["pay_amt1"]
    PAY_AMT2 = request.form["pay_amt2"]
    PAY_AMT3 = request.form["pay_amt3"]
    PAY_AMT4 = request.form["pay_amt4"]
    PAY_AMT5 = request.form["pay_amt5"]
    PAY_AMT6 = request.form["pay_amt6"]

    input_dict={'ID':2,
                 'SEX':[Gender],
                 'EDUCATION':[Education],
                 'MARRIAGE':[Marital_status],
                 'AGE':[Age],
                 'LIMIT_BAL':[Limit_balance],
                 'PAY_1':[PAY_1],
                 'PAY_2':[PAY_2],
                 'PAY_3':[PAY_3],
                 'PAY_4':[PAY_4],
                 'PAY_5':[PAY_5],
                 'PAY_6':[PAY_6],
                 'BILL_AMT1':[BILL_AMT1],
                 'BILL_AMT2':[BILL_AMT2],
                 'BILL_AMT3':[BILL_AMT3],
                 'BILL_AMT4':[BILL_AMT4],
                 'BILL_AMT5':[BILL_AMT5],
                 'BILL_AMT6':[BILL_AMT6],
                 'PAY_AMT1':[PAY_AMT1],
                 'PAY_AMT2':[PAY_AMT2],
                 'PAY_AMT3':[PAY_AMT3],
                 'PAY_AMT4':[PAY_AMT4],
                 'PAY_AMT5':[PAY_AMT5],
                 'PAY_AMT6':[PAY_AMT6],
            }
    input_df = pd.DataFrame(input_dict)
    logging.info(f"Input : {input_df}")

    saved_model_path = "E:/Ineuron ML Projects/Internship Projects/Creditcard defaulter/saved_models/1704008855/model.pkl"
    rfc_cl = load_object(file_path= saved_model_path)

    prediction = rfc_cl.predict(input_df)
    logging.info(f"Result : {prediction}")
    result = ""
    if prediction == 1:
        result = "The Credit card holder will be Defaulter in the next month"
    else:
        result = "The Credit card holder will not be Defaulter in the next month"

    return render_template('index.html', prediction_text = result)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8080) #for deployment run
    # app.run(host="127.0.0.1", port=8080,debug=True) # for local run
