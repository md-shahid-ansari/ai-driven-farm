from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI', '')

# Initialize PyMongo without an app (to be initialized later)
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})

    # Set MongoDB URI
    app.config["MONGO_URI"] = MONGO_URI

    # Initialize PyMongo with the app
    mongo.init_app(app) 
    print(" * Database :", mongo.db.name)

    # Register the main routes 
    from app.routes import admin
    app.register_blueprint(admin)

    return app

def get_db():
    return mongo.db