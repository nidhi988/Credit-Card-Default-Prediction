#!/usr/bin/env python
# coding: utf-8



import os
import sys
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact

from src.exception import CustomException

from src.utils import save_object

try:
    from src.logger import logging
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            import logging   # ✅ 🔥 CRITICAL FIX (local import)

            logging.info("Starting feature engineering")

            df = df.copy()

            if "ID" in df.columns:
                df.drop(columns=["ID"], inplace=True)

            pay_cols = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
            bill_cols = ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]
            pay_amt_cols = ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]

            required_cols = pay_cols + bill_cols + pay_amt_cols + ["LIMIT_BAL"]

            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise CustomException(f"Missing columns: {missing_cols}", sys)

            df["AVG_PAY_STATUS"] = df[pay_cols].mean(axis=1)
            df["MAX_PAY_STATUS"] = df[pay_cols].max(axis=1)
            df["DELAY_COUNT"] = (df[pay_cols] > 0).sum(axis=1)

            df["TOTAL_BILL_AMT"] = df[bill_cols].sum(axis=1)
            df["AVG_BILL_AMT"] = df[bill_cols].mean(axis=1)

            df["TOTAL_PAY_AMT"] = df[pay_amt_cols].sum(axis=1)
            df["AVG_PAY_AMT"] = df[pay_amt_cols].mean(axis=1)

            df["BILL_TO_LIMIT_RATIO"] = df["TOTAL_BILL_AMT"] / df["LIMIT_BAL"].replace(0, 1)
            df["PAY_TO_BILL_RATIO"] = df["TOTAL_PAY_AMT"] / df["TOTAL_BILL_AMT"].replace(0, 1)

            logging.info("Feature engineering completed")

            return df

        except Exception as e:
            raise CustomException(e, sys)
    
    
    

    def get_preprocessor(self):
        try:
            return Pipeline([
                ("feature_engineering", FunctionTransformer(self.create_features, validate=False))
            ])
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            logging.info("Starting data transformation")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            target_column = "DEFAULT_PAYMENT_NEXT_MONTH"

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            preprocessor = self.get_preprocessor()

            # 🔥 IMPORTANT: FunctionTransformer RETURNS DataFrame → keep it
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            # ✅ Ensure it's DataFrame (safety)
            if not isinstance(X_train_transformed, pd.DataFrame):
                raise CustomException("Preprocessor must return DataFrame", sys)

            # 🔥 Save correct feature names
            preprocessor.feature_names_ = list(X_train_transformed.columns)

            # Add target
            X_train_transformed[target_column] = y_train.values
            X_test_transformed[target_column] = y_test.values

            # Create dirs
            os.makedirs(os.path.dirname(self.config.transformed_train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.transformed_test_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.preprocessor_obj_file_path), exist_ok=True)

            # Save CSV
            X_train_transformed.to_csv(self.config.transformed_train_file_path, index=False)
            X_test_transformed.to_csv(self.config.transformed_test_file_path, index=False)

            # Save preprocessor
            save_object(self.config.preprocessor_obj_file_path, preprocessor)

            logging.info("Transformation completed successfully")

            return DataTransformationArtifact(
                transformed_train_file_path=self.config.transformed_train_file_path,
                transformed_test_file_path=self.config.transformed_test_file_path,
                preprocessor_file_path=self.config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)


# ✅ Standalone test
if __name__ == "__main__":
    try:
        from src.entity.config_entity import DataTransformationConfig, DataIngestionConfig

        ingestion_config = DataIngestionConfig()
        transformation_config = DataTransformationConfig()

        transformer = DataTransformation(transformation_config)

        train_path = ingestion_config.train_data_path
        test_path = ingestion_config.test_data_path

        artifact = transformer.initiate_data_transformation(train_path, test_path)

        print("\n✅ Data Transformation Completed\n")
        print(artifact)

    except Exception as e:
        print(e)