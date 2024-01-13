import os
from pymongo import MongoClient
from dotenv import load_dotenv

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):
        load_dotenv()

        mongo_db_name = os.getenv('MONGO_DB_NAME')
        mongo_host = os.getenv('MONGO_HOST')
        mongo_port = int(os.getenv('MONGO_PORT'))

        self.client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
        self.db = self.client[mongo_db_name]