#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from dataclasses import dataclass, field

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

@dataclass
class DataIngestionConfig:
    root_dir: str = os.path.join(PROJECT_ROOT, "artifacts")
    raw_data_path: str = os.path.join(PROJECT_ROOT, "artifacts", "raw.csv")
    train_data_path: str = os.path.join(PROJECT_ROOT, "artifacts", "train.csv")
    test_data_path: str = os.path.join(PROJECT_ROOT, "artifacts", "test.csv")

    # Astra DB config
    keyspace: str = "default_keyspace"
    table_name: str = "credit_default_data"
    secure_connect_bundle: str = os.path.join(
        PROJECT_ROOT, "config", "secure-connect-database.zip"
    )

    # 🔥 IMPORTANT FIX
    client_id: str = "token"
    client_secret: str = os.getenv(
        "ASTRA_DB_TOKEN",
        "AstraCS:ZqFMwbQuZftxNIXGJXcSDvPi:708b91773c1452d37ef49648ca3dd735ab0d0475eb282a08261409adba87b7d3"
    )


@dataclass
class DataValidationConfig:
    root_dir: str = os.path.join(PROJECT_ROOT, "artifacts")
    train_data_path: str = os.path.join(PROJECT_ROOT, "artifacts", "train.csv")
    test_data_path: str = os.path.join(PROJECT_ROOT, "artifacts", "test.csv")
    status_file: str = os.path.join(PROJECT_ROOT, "artifacts", "data_validation_status.txt")
    required_columns: list = field(default_factory=lambda: [
        "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
        "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
        "BILL_AMT1", "BILL_AMT2", "BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6",
        "PAY_AMT1", "PAY_AMT2", "PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6",
        "DEFAULT_PAYMENT_NEXT_MONTH"
    ])


@dataclass
class DataTransformationConfig:
    root_dir: str = os.path.join(PROJECT_ROOT, "artifacts")
    transformed_train_file_path: str = os.path.join(PROJECT_ROOT, "artifacts", "train_transformed.csv")
    transformed_test_file_path: str = os.path.join(PROJECT_ROOT, "artifacts", "test_transformed.csv")
    preprocessor_obj_file_path: str = os.path.join(PROJECT_ROOT, "artifacts", "preprocessor.pkl")
    target_column: str = "DEFAULT_PAYMENT_NEXT_MONTH"


@dataclass
class ModelTrainerConfig:
    root_dir: str = os.path.join(PROJECT_ROOT, "artifacts")
    trained_model_file_path: str = os.path.join(PROJECT_ROOT, "artifacts", "model.pkl")
    expected_accuracy: float = 0.70
    target_column: str = "DEFAULT_PAYMENT_NEXT_MONTH"



# In[ ]:




