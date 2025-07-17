from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['library_db']
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")


