


import os
import sys
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from sklearn.model_selection import train_test_split

# ❌ REMOVE this (bad practice in modules)
# os.chdir(r"C:\Users\nidhi\Desktop\credit_default_project")

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

from src.exception import CustomException
from src.logger import logging


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        # ✅ Config = instructions (paths, credentials)
        self.ingestion_config = config

    def connect_to_cassandra(self):
        try:
            cloud_config = {
                "secure_connect_bundle": self.ingestion_config.secure_connect_bundle
            }

            auth_provider = PlainTextAuthProvider(
                self.ingestion_config.client_id,
                self.ingestion_config.client_secret
            )

            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()

            logging.info("Connected to Cassandra successfully")
            return cluster, session

        except Exception as e:
            # ❌ DON'T pass None → breaks traceback
            raise CustomException(e, sys)

    def fetch_data_from_cassandra(self):
        cluster = None
        session = None
        try:
            cluster, session = self.connect_to_cassandra()
            session.set_keyspace(self.ingestion_config.keyspace)

            query = f"SELECT * FROM {self.ingestion_config.table_name};"
            rows = session.execute(query)

            df = pd.DataFrame(list(rows))

            logging.info(f"Data fetched with shape: {df.shape}")
            return df

        except Exception as e:
            raise CustomException(e, sys)

        finally:
            if session:
                session.shutdown()
            if cluster:
                cluster.shutdown()

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion")

            df = self.fetch_data_from_cassandra()

            # ✅ STANDARDIZE COLUMN NAMES (VERY IMPORTANT)
            df.columns = df.columns.str.upper().str.strip()

            # ✅ FIX TARGET COLUMN NAME
            if "DEFAULT.PAYMENT.NEXT.MONTH" in df.columns:
                df.rename(columns={
                    "DEFAULT.PAYMENT.NEXT.MONTH": "DEFAULT_PAYMENT_NEXT_MONTH"
                }, inplace=True)

            target_col = "DEFAULT_PAYMENT_NEXT_MONTH"

            if target_col not in df.columns:
                raise CustomException(f"{target_col} not found in dataset", sys)

            # ✅ CREATE ALL DIRECTORIES
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)

            # ✅ SAVE RAW DATA
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Raw data saved at {self.ingestion_config.raw_data_path}")

            # ✅ TRAIN-TEST SPLIT
            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42,
                stratify=df[target_col]
            )

            # ✅ SAVE SPLIT DATA
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info("Train & Test data saved successfully")

            # ✅ RETURN ARTIFACT (CORRECT)
            return DataIngestionArtifact(
                train_file_path=self.ingestion_config.train_data_path,
                test_file_path=self.ingestion_config.test_data_path,
                raw_file_path=self.ingestion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)


# ✅ EXECUTION BLOCK (for standalone testing only)
if __name__ == "__main__":
    try:
        config = DataIngestionConfig()
        ingestion = DataIngestion(config)

        artifact = ingestion.initiate_data_ingestion()

        print("✅ Data Ingestion Completed")
        print(artifact)

    except Exception as e:
        print(e)