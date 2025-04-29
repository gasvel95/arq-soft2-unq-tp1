from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

MONGO_URI = os.getenv("MONGO_URI") 

client = MongoClient("mongodb+srv://gastonveliez95:G3l0E6iZc5LuagC5@clusterarq2.z5kcuim.mongodb.net/?retryWrites=true&w=majority&appName=ClusterArq2", server_api=ServerApi('1'))
db = client["marketplace_db"]
