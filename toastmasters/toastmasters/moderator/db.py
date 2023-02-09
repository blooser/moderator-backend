from pymongo import MongoClient


class Mongo:
    CONNECTION_STRING = "mongodb://localhost:27017/"

    def __init__(self):
        self.client = MongoClient(self.CONNECTION_STRING)
        self.db_handle = self.client["test"]

    
