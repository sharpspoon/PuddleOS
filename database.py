from flask import Flask, render_template, request, redirect, url_for, Blueprint
import uuid
import json
from pymongo import MongoClient


bp = Blueprint('database', __name__, url_prefix='/database')

@bp.route('/load/<dataset_id>', methods=['GET'])
def load_dataset(dataset_id):
    print("Got request to load dataset " + dataset_id)
    return redirect(url_for('index'))

@bp.route('/save', methods=['POST'])
def save_dataset():
    print("Got request to save dataset")
    return redirect(url_for('index'))

def get_user_data(user_id: uuid):
    print("Got request to get user data for user " + str(user_id))
    data = None
    try:
        with open("d3.json") as f:
                data = json.load(f)
    except FileNotFoundError:  
        print("Data json not found, exiting...")
        exit(1)
    return data

def create_user_data(user_id: uuid):
    print("Got request to create user data for user " + str(user_id))
    return 