from random import randint
from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    MONGO_URL = os.getenv('MONGO_URL')
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client.test
    try:
        print("Successfully connected to MongoDB")
    except Exception:
        print("Unable to connect to the server.")

    tosave = { "name": "MongoDB", "type": "database", "count": 1, "info": { "x": randint(1,10), "y": randint(1,10)} }
    db.test.insert_one(tosave)
    print("Inserted the document into the collection")

    cursor = db.test.find()
    for doc in cursor:
        pprint(doc)

if __name__ == "__main__":
    main()