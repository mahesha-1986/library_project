from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['library']
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")


