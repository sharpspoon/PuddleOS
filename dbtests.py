from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    MONGO_URL = os.getenv('MONGO_URL')
    print(MONGO_URL)
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

    
    try:
        pprint(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
    # db = client.admin
    # serverStatusResult=db.command("serverStatus")
    # pprint(serverStatusResult)

if __name__ == "__main__":
    main()