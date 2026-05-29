#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import sys

# ✅ VERY IMPORTANT (fixes import issues in Flask)
sys.path.append(os.path.abspath("."))

from flask import Flask, request, render_template
import pandas as pd

from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
from src.exception import CustomException   # ✅ consistent error handling

app = Flask(__name__)


# 🏠 Home route
@app.route("/")
def index():
    return render_template("index.html")


# 🔥 Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form

        # ✅ Convert input safely
        custom_data = CustomData(
            LIMIT_BAL=float(data.get("LIMIT_BAL", 0)),
            SEX=int(data.get("SEX", 0)),
            EDUCATION=int(data.get("EDUCATION", 0)),
            MARRIAGE=int(data.get("MARRIAGE", 0)),
            AGE=int(data.get("AGE", 0)),
            PAY_0=int(data.get("PAY_0", 0)),
            PAY_2=int(data.get("PAY_2", 0)),
            PAY_3=int(data.get("PAY_3", 0)),
            PAY_4=int(data.get("PAY_4", 0)),
            PAY_5=int(data.get("PAY_5", 0)),
            PAY_6=int(data.get("PAY_6", 0)),
            BILL_AMT1=float(data.get("BILL_AMT1", 0)),
            BILL_AMT2=float(data.get("BILL_AMT2", 0)),
            BILL_AMT3=float(data.get("BILL_AMT3", 0)),
            BILL_AMT4=float(data.get("BILL_AMT4", 0)),
            BILL_AMT5=float(data.get("BILL_AMT5", 0)),
            BILL_AMT6=float(data.get("BILL_AMT6", 0)),
            PAY_AMT1=float(data.get("PAY_AMT1", 0)),
            PAY_AMT2=float(data.get("PAY_AMT2", 0)),
            PAY_AMT3=float(data.get("PAY_AMT3", 0)),
            PAY_AMT4=float(data.get("PAY_AMT4", 0)),
            PAY_AMT5=float(data.get("PAY_AMT5", 0)),
            PAY_AMT6=float(data.get("PAY_AMT6", 0)),
        )

        df = custom_data.get_data_as_dataframe()

        pipeline = PredictionPipeline()
        prediction = pipeline.predict(df)[0]

        # ✅ Human readable output
        result = "Will Default ❌" if prediction == 1 else "Will NOT Default ✅"

        return render_template("index.html", prediction_text=result)

    except CustomException as ce:
        return render_template("index.html", prediction_text=f"Error: {ce}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"Unexpected Error: {str(e)}")


# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True)