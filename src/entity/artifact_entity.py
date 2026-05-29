#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    raw_file_path: str
    train_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    message: str = ""


@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_file_path: str


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric: float
    test_metric: float


# In[ ]:




