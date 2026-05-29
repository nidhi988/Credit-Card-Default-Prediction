import os
import sys
import pandas as pd

from src.exception import CustomException   # ✅ IMPORTANT FIX
from src.logger import logging
from src.utils import load_object

print("✅🔥 prediction_pipeline file is running")


class PredictionPipeline:
    def __init__(self):
        try:
            logging.info("Loading model and preprocessor")

            self.model = load_object(os.path.join("artifacts", "model.pkl"))
            self.preprocessor = load_object(os.path.join("artifacts", "preprocessor.pkl"))

            logging.info("Model and preprocessor loaded successfully")

        except Exception as e:
            raise CustomException(e, sys)   # ✅ FIX


    def predict(self, features: pd.DataFrame):
        try:
            logging.info("Starting prediction")

            # ✅ Apply SAME transformation
            transformed = self.preprocessor.transform(features)

            # ✅ Ensure DataFrame format
            if not isinstance(transformed, pd.DataFrame):
                transformed = pd.DataFrame(
                    transformed,
                    columns=self.preprocessor.feature_names_
                )

            # ✅ Ensure SAME column order
            transformed = transformed[self.preprocessor.feature_names_]

            predictions = self.model.predict(transformed)

            logging.info("Prediction completed")

            return predictions

        except Exception as e:
            raise CustomException(e, sys)   # ✅ FIX


# 🔥 User input handler
class CustomData:
    def __init__(self, **kwargs):
        self.data = kwargs

    def get_data_as_dataframe(self):
        try:
            return pd.DataFrame([self.data])
        except Exception as e:
            raise CustomException(e, sys)


# 🔥 Standalone testing
if __name__ == "__main__":
    try:
        test_data = CustomData(
            LIMIT_BAL=20000, SEX=2, EDUCATION=2, MARRIAGE=1, AGE=25,
            PAY_0=0, PAY_2=0, PAY_3=0, PAY_4=0, PAY_5=0, PAY_6=0,
            BILL_AMT1=3913, BILL_AMT2=3102, BILL_AMT3=689,
            BILL_AMT4=0, BILL_AMT5=0, BILL_AMT6=0,
            PAY_AMT1=0, PAY_AMT2=689, PAY_AMT3=0,
            PAY_AMT4=0, PAY_AMT5=0, PAY_AMT6=0
        )

        df = test_data.get_data_as_dataframe()

        pipeline = PredictionPipeline()
        result = pipeline.predict(df)

        print("\nPrediction:", result[0])

    except Exception as e:
        print(e)