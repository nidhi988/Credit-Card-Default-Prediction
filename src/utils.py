#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import sys
import dill

from src.exception import CustomException
from src.logger import logging


def save_object(file_path: str, obj):
    try:
        # ✅ Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info(f"Object saved at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: str):
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"File not found: {file_path}", sys)

        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info(f"Object loaded from: {file_path}")

        return obj

    except Exception as e:
        raise CustomException(e, sys)


# In[ ]:




