# Credit card Defaulter Prediction

## Problem Statement
Financial threats are displaying a trend about the credit risk of commercial banks as the
incredible improvement in the financial industry has arisen. In this way, one of the
biggest threats faces by commercial banks is the risk prediction of credit clients. The
goal is to predict the probability of credit default based on credit card owner's
characteristics and payment history.

## Approach
The classical machine learning tasks like Data Exploration, Data Cleaning,
Feature Engineering, Model Building and Model Testing. Try out different machine
learning algorithms that’s best fit for the above case.

## Tech Stack Used
1. Python 
2. Flask
3. HTML,CSS 
3. Machine learning algorithms

## Infrastructure Required.

1. AWS EC2
2. AWS ECR
3. Git Actions
4. Docker

## How to run?
Before we run the project, we need AWS account to access the service like ECR and EC2 instances.


## Project Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)


## Deployment Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)


### Step 1: Clone the repository
```bash
git clone https://github.com/geddadasuresh84326/credit-card-defaulter
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n credit_env python=3.8 -y
```

```bash
conda activate credit_env
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>


```

### Step 5 - Run the application server
```bash
python app.py
```


