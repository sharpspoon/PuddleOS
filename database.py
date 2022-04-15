from flask import Flask, render_template, request, redirect, url_for, Blueprint
from datetime import datetime
import uuid
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
user_sessions = mongo_client.dev.user_sessions

bp = Blueprint('database', __name__, url_prefix='/database')

@bp.route('/load/<dataset_id>', methods=['GET'])
def load_dataset(dataset_id):
    # print("Got request to load dataset " + dataset_id)
    return redirect(url_for('index'))

@bp.route('/save', methods=['POST'])
def save_dataset():
    # print("Got request to save dataset")
    return redirect(url_for('index'))

def get_user_data(user_id: uuid):
    # print("Got request to get user data for user " + str(user_id))
    user_data = user_sessions.find_one({'user_id': str(user_id)})
    if not user_data:
        create_user_data(user_id)
        user_data = user_sessions.find_one({'user_id': str(user_id)})
    return user_data['data']

def create_user_data(user_id: uuid):
    # print("Got request to create user data for user " + str(user_id))
    data = None
    try:
        with open("d3.json") as f:
                data = json.load(f)
    except FileNotFoundError:  
        print("Data json not found, exiting...")
        exit(1)
    # createdAt is used to allow the data to expire 
    user_sessions.insert_one({'user_id': str(user_id), 'createdAt': datetime.today().replace(microsecond=0),'data': data})
    return 

def update_user_data(user_id: uuid, data):
    # print("Got request to update user data for user " + str(user_id))
    res = user_sessions.update_one({'user_id': str(user_id)}, {'$set': {'data': data}})
    # print("Updated user data for user " + str(user_id) + ": " + str(res.modified_count))
    return