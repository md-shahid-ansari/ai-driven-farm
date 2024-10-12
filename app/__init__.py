from flask import Flask
from flask_pymongo import PyMongo, MongoClient
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

    # Set MongoDB URI
    app.config["MONGO_URI"] = MONGO_URI

    # Initialize PyMongo with the app
    mongo.init_app(app) 
    print(" * Database :", mongo.db.name)

    # Register the main routes (make sure routes.py exists and is correctly set up)
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app

def get_db():
    return mongo.db