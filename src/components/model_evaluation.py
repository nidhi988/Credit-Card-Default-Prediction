#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import sys
import pandas as pd
from dataclasses import dataclass

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
from src.entity.artifact_entity import DataTransformationArtifact


# ✅ Proper config
@dataclass
class ModelEvaluationConfig:
    model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig = ModelEvaluationConfig()):
        self.config = config

    def initiate_model_evaluation(
        self,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            logging.info("Starting model evaluation")

            # ✅ Load model
            model = load_object(self.config.model_file_path)
            logging.info(f"Model loaded from {self.config.model_file_path}")

            # ✅ Load transformed test data
            test_df = pd.read_csv(
                data_transformation_artifact.transformed_test_file_path
            )

            # ✅ Split features & target
            X_test = test_df.iloc[:, :-1]
            y_test = test_df.iloc[:, -1]

            logging.info("Test data prepared")

            # ✅ Predictions
            y_pred = model.predict(X_test)

            # ✅ Probability for ROC-AUC
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
            else:
                y_prob = y_pred

            # ✅ Metrics (safe)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y_test, y_prob)
            cm = confusion_matrix(y_test, y_pred)

            # ✅ PRINT OUTPUT
            print("\n================ MODEL EVALUATION RESULTS ================\n")
            print(f"Accuracy      : {accuracy:.4f}")
            print(f"Precision     : {precision:.4f}")
            print(f"Recall        : {recall:.4f}")
            print(f"F1 Score      : {f1:.4f}")
            print(f"ROC-AUC Score : {roc_auc:.4f}")
            print("\nConfusion Matrix:")
            print(cm)
            print("\n==========================================================\n")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "roc_auc": roc_auc
            }

        except Exception as e:
            raise CustomException(e, sys)


# ✅ Standalone testing
if __name__ == "__main__":
    try:
        from src.entity.artifact_entity import DataTransformationArtifact

        artifact = DataTransformationArtifact(
            transformed_train_file_path="artifacts/train_transformed.csv",
            transformed_test_file_path="artifacts/test_transformed.csv",
            preprocessor_file_path="artifacts/preprocessor.pkl"
        )

        evaluator = ModelEvaluation()
        result = evaluator.initiate_model_evaluation(artifact)

        print("\nReturned Result Dictionary:")
        print(result)

    except Exception as e:
        print(e)