#!/usr/bin/env python
# coding: utf-8

# In[1]



# In[3]:



import sys
import os
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils import save_object


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(
        self,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            logging.info("Starting model training process")

            # ✅ Load transformed data
            train_df = pd.read_csv(
                data_transformation_artifact.transformed_train_file_path
            )
            test_df = pd.read_csv(
                data_transformation_artifact.transformed_test_file_path
            )

            logging.info("Transformed train and test data loaded")

            # ✅ Target column (KEEP CONSISTENT EVERYWHERE)
            target_column = "DEFAULT_PAYMENT_NEXT_MONTH"

            if target_column not in train_df.columns:
                raise CustomException(f"{target_column} not found in train data", sys)

            if target_column not in test_df.columns:
                raise CustomException(f"{target_column} not found in test data", sys)

            # ✅ Remove ID if exists (safety)
            drop_cols = ["ID"] if "ID" in train_df.columns else []

            # ✅ Split features and target
            X_train = train_df.drop(columns=[target_column] + drop_cols, errors="ignore")
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column] + drop_cols, errors="ignore")
            y_test = test_df[target_column]

            logging.info("Feature-target split completed")

            # ✅ Models
            models = {
                "LogisticRegression": LogisticRegression(max_iter=3000),
                "RandomForest": RandomForestClassifier(random_state=42)
            }

            model_report = {}

            # ✅ Train & evaluate
            for model_name, model in models.items():
                logging.info(f"Training model: {model_name}")

                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)

                model_report[model_name] = accuracy

                logging.info(f"{model_name} Accuracy: {accuracy}")

            # ✅ Select best model
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            logging.info(f"Best model selected: {best_model_name}")

            # ✅ Ensure directory exists
            os.makedirs(
                os.path.dirname(self.config.trained_model_file_path),
                exist_ok=True
            )

            # ✅ Save model
            save_object(self.config.trained_model_file_path, best_model)

            logging.info(
                f"Model saved at: {self.config.trained_model_file_path}"
            )

            return best_model_name, model_report

        except Exception as e:
            raise CustomException(e, sys)


# ✅ Standalone testing
if __name__ == "__main__":
    try:
        from src.entity.config_entity import ModelTrainerConfig
        from src.entity.artifact_entity import DataTransformationArtifact

        config = ModelTrainerConfig()
        trainer = ModelTrainer(config)

        transformation_artifact = DataTransformationArtifact(
            transformed_train_file_path="artifacts/train_transformed.csv",
            transformed_test_file_path="artifacts/test_transformed.csv",
            preprocessor_file_path="artifacts/preprocessor.pkl"
        )

        result = trainer.initiate_model_trainer(transformation_artifact)

        print("\n✅ Model Training Completed\n")
        print("Best Model:", result[0])
        print("Model Report:", result[1])

    except Exception as e:
        print(e)