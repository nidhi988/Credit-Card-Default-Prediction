#!/usr/bin/env python
# coding: utf-8

# In[4]:




import os
import sys
import pandas as pd

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact

from src.exception import CustomException
from src.logger import logging


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_file_exists(self):
        try:
            logging.info("Checking if train and test files exist")

            if not os.path.exists(self.config.train_data_path):
                raise CustomException("Train file not found", sys)

            if not os.path.exists(self.config.test_data_path):
                raise CustomException("Test file not found", sys)

            logging.info("Both train and test files found")
            return True

        except Exception as e:
            raise CustomException(e, sys)

    def validate_columns(self, df: pd.DataFrame):
        try:
            logging.info("Validating required columns")

            # ✅ STANDARDIZE (important for safety)
            df.columns = df.columns.str.upper().str.strip()

            required_cols = [col.upper() for col in self.config.required_columns]

            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                raise CustomException(f"Missing columns: {missing_cols}", sys)

            logging.info("All required columns are present")
            return True

        except Exception as e:
            raise CustomException(e, sys)

    def check_missing_values(self, df: pd.DataFrame):
        try:
            logging.info("Checking for missing values")

            missing_count = df.isnull().sum().sum()

            if missing_count > 0:
                logging.warning(f"Dataset contains {missing_count} missing values")
            else:
                logging.info("No missing values found")

            return missing_count

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self):
        try:
            logging.info("Starting data validation")

            # ✅ Step 1: Check files
            self.validate_file_exists()

            # ✅ Step 2: Load data
            train_df = pd.read_csv(self.config.train_data_path)
            test_df = pd.read_csv(self.config.test_data_path)

            # ✅ Step 3: Validate columns
            self.validate_columns(train_df)
            self.validate_columns(test_df)

            # ✅ Step 4: Missing values
            train_missing = self.check_missing_values(train_df)
            test_missing = self.check_missing_values(test_df)

            logging.info("Data validation completed successfully")

            return DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=self.config.train_data_path,
                valid_test_file_path=self.config.test_data_path,
                message=f"Train missing: {train_missing}, Test missing: {test_missing}"
            )

        except Exception as e:
            raise CustomException(e, sys)


# ✅ Standalone test
if __name__ == "__main__":
    try:
        config = DataValidationConfig()
        validator = DataValidation(config)

        artifact = validator.initiate_data_validation()

        print("\n✅ Data Validation Completed\n")
        print("Status :", artifact.validation_status)
        print("Train  :", artifact.valid_train_file_path)
        print("Test   :", artifact.valid_test_file_path)
        print("Msg    :", artifact.message)

    except Exception as e:
        print(e)