#  Credit Default Prediction - End-to-End Machine Learning Project

An end-to-end Machine Learning project that predicts whether a customer is likely to default on credit card payment using customer financial and repayment history data.

This project demonstrates a modular industry-style ML pipeline including:

* Data Ingestion
* Data Validation
* Feature Engineering
* Data Transformation
* Model Training
* Model Evaluation
* Prediction Pipeline
* Flask Deployment

---

# Project Overview

The goal of this project is to build a complete ML workflow capable of:

* Loading data from Cassandra Database
* Validating dataset structure
* Performing feature engineering
* Training multiple ML models
* Evaluating model performance
* Saving trained artifacts
* Serving predictions through a Flask web application

---

# 📁 Project Structure

credit_default_project/

│

├── artifacts/

│   ├── raw.csv

│   ├── train.csv

│   ├── test.csv

│   ├── train_transformed.csv

│   ├── test_transformed.csv

│   ├── model.pkl

│   ├── preprocessor.pkl

│   └── logs/

│

├── config/

│   └── secure-connect-database.zip

│

├── notebook/

│   └── eda.ipynb

│

├── src/

│   ├── components/

│   │   ├── data_ingestion.py

│   │   ├── data_validation.py

│   │   ├── data_transformation.py

│   │   ├── model_trainer.py

│   │   └── model_evaluation.py

│   │

│   ├── entity/

│   │   ├── config_entity.py

│   │   └── artifact_entity.py

│   │

│   ├── pipeline/

│   │   └── prediction_pipeline.py

│   │

│   ├── logger/

│   │   └── logger.py

│   │

│   ├── exception/

│   │   └── exception.py

│   │

│   └── utils.py

│

├── templates/

│   └── index.html

│

├── app.py

├── requirements.txt

└── README.md
```

---

#  Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Flask
* Cassandra Database
* Dill
* HTML

---

#  ML Pipeline Workflow

## 1️⃣ Data Ingestion

* Connects to Cassandra DB
* Fetches dataset
* Saves raw dataset
* Splits into train/test data

## 2️⃣ Data Validation

* Checks file existence
* Validates required columns
* Checks missing values

## 3️⃣ Data Transformation

* Feature Engineering
* Ratio-based features
* Aggregated payment/bill features
* Saves transformed datasets
* Saves preprocessing pipeline

## 4️⃣ Model Training

Models Used:

* Logistic Regression
* Random Forest Classifier

The best-performing model is selected automatically based on accuracy.

## 5️⃣ Model Evaluation

Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC Score
* Confusion Matrix

## 6️⃣ Prediction Pipeline

* Loads saved model and preprocessor
* Applies same transformations to new data
* Generates real-time predictions

## 7️⃣ Flask Deployment

A local Flask web application is used for:

* Taking user inputs
* Running prediction pipeline
* Displaying prediction result

---

# Feature Engineering Performed

Created custom features such as:

* Average Payment Status
* Maximum Delay Status
* Delay Count
* Total Bill Amount
* Average Bill Amount
* Total Payment Amount
* Bill-to-Limit Ratio
* Pay-to-Bill Ratio

---

#  Model Output

Prediction Results:

* Will Default ❌
* Will NOT Default ✅

---

#  Logging & Exception Handling

Custom logging and exception handling system implemented for:

* Easier debugging
* Error traceability
* Production-style monitoring

---

#  How to Run Project

## 1️⃣ Clone Repository


git clone <your-repository-link>
```

---

## 2️⃣ Install Requirements


pip install -r requirements.txt
```

---

## 3️⃣ Run Flask Application

python app.py
```

---

## 4️⃣ Open Browser

http://127.0.0.1:5000


Author

Nidhi Lohani

Applied Machine Learning Engineer

Python | Scikit-learn | ML Pipelines | Feature Engineering

---
