from pymongo import MongoClient
import os
from dotenv import load_dotenv

def initialize():
    load_dotenv()
    # Get MongoDB connection details from environment variables
    mongo_db_name = os.getenv('MONGO_DB_NAME')
    mongo_host = os.getenv('MONGO_HOST')
    mongo_port = int(os.getenv('MONGO_PORT'))

    # Connect to MongoDB
    client = MongoClient(host=mongo_host, port=mongo_port)

    db = None
    # Check if the database already exists
    if mongo_db_name in client.list_database_names():
        print(f"Database '{mongo_db_name}' already exists.")
    else:
        # Create the database
        db = client[mongo_db_name]
        print(f"Database '{mongo_db_name}' created.")

        adventures = db.create_collection('adventures')
        db.create_collection('games_history')

        default_adventure = {
            'type': 'default',
            'name': 'Not another clone of Fallout',
            'description': 'World after nuclear war',
            'character_description': 'A lone raider, trying to survive',
            'avatar_description': 'a fat man wearing a funny white hat'
        }

        adventures.insert_one(default_adventure)

    client.close()
