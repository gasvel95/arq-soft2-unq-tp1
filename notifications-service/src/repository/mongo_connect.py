from pathlib import Path
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi

client = None
db = None

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
MONGO_URI = os.getenv("MONGO_URI") 

def get_client():
    global client
    if client is None:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    return client

def db_selection(client):
    global db
    if db is None:
        return client["marketplace_db"]
    return client["test_db"]

client = get_client()
db = db_selection(client)