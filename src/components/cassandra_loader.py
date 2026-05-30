#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
print(os.getcwd())


# In[3]:


os.chdir(r"C:\Users\nidhi\Desktop\credit_default_project")


# In[4]:


os.getcwd()


# In[6]:


import sys
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import BatchStatement

from src.entity import DataIngestionConfig
from src.exception import CustomException
from src.logger import logging


class CassandraLoader:
    def __init__(self):
        self.config = DataIngestionConfig()

    def connect(self):
        try:
            cloud_config = {
                "secure_connect_bundle": self.config.secure_connect_bundle
            }

            # ✅ FIXED AUTH
            auth_provider = PlainTextAuthProvider(
                self.config.client_id,
                self.config.client_secret
            )

            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()

            logging.info("Connected to Cassandra successfully")
            return cluster, session

        except Exception as e:
            raise CustomException(e, None)

    def create_table(self, session):
        try:
            # ❌ DO NOT CREATE KEYSPACE IN ASTRA
            session.set_keyspace(self.config.keyspace)

            session.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.config.table_name} (
                    ID int PRIMARY KEY,
                    LIMIT_BAL float,
                    SEX int,
                    EDUCATION int,
                    MARRIAGE int,
                    AGE int,
                    PAY_0 int,
                    PAY_2 int,
                    PAY_3 int,
                    PAY_4 int,
                    PAY_5 int,
                    PAY_6 int,
                    BILL_AMT1 float,
                    BILL_AMT2 float,
                    BILL_AMT3 float,
                    BILL_AMT4 float,
                    BILL_AMT5 float,
                    BILL_AMT6 float,
                    PAY_AMT1 float,
                    PAY_AMT2 float,
                    PAY_AMT3 float,
                    PAY_AMT4 float,
                    PAY_AMT5 float,
                    PAY_AMT6 float,
                    default_payment_next_month int
                );
            """)

            logging.info("Table created or already exists")

        except Exception as e:
            raise CustomException(e, None)

    def load_csv_to_cassandra(self, csv_path: str):
        cluster = None

        try:
            cluster, session = self.connect()
            self.create_table(session)

            df = pd.read_csv(csv_path)
            logging.info(f"CSV loaded successfully with shape: {df.shape}")

            # ✅ Ensure correct column order
            columns = [
                "id", "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
                "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
                "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
                "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6",
                "default_payment_next_month"
            ]

            df = df[columns]

            insert_query = session.prepare(f"""
                INSERT INTO {self.config.table_name} (
                    id, LIMIT_BAL, SEX, EDUCATION, MARRIAGE, AGE,
                    PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6,
                    BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5, BILL_AMT6,
                    PAY_AMT1, PAY_AMT2, PAY_AMT3, PAY_AMT4, PAY_AMT5, PAY_AMT6,
                    default_payment_next_month
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)

            batch = BatchStatement()
            batch_size = 100

            for _, row in df.iterrows():
                batch.add(insert_query, tuple(row))

                if len(batch) >= batch_size:
                    session.execute(batch)
                    batch = BatchStatement()

            if len(batch) > 0:
                session.execute(batch)

            logging.info("CSV data loaded into Cassandra successfully")

        except Exception as e:
            raise CustomException(e, None)

        finally:
            if cluster:
                cluster.shutdown()
                logging.info("Cassandra connection closed")


# In[7]:


loader = CassandraLoader()
loader.load_csv_to_cassandra(r"C:\Users\nidhi\Desktop\credit_default_project\artifacts\eda_processed.csv")


# In[ ]:




