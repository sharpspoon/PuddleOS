from random import randint
from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    MONGO_URL = os.getenv('MONGO_URL')
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client.dev

    db.drop_collection('user_sessions')
    db.create_collection('user_sessions')
    db.user_sessions.create_index([('user_id', 1)], unique=True)
    # make user_id data expire after 1 day 
    db.user_sessions.create_index([('createdAt', 1)], expireAfterSeconds=60*60*24)

if __name__ == "__main__":
    main()