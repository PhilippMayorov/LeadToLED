import os
import urllib.parse
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import configparser
from datetime import datetime

load_dotenv()

# Load configuration
config = configparser.ConfigParser()
config.read('config.properties')

# Encode the password to handle special characters


password = "digiPenPassword"
username = "philipp"

uri = os.getenv("uri")

# Establish a MongoDB connection
print("Before Client")

client = MongoClient(
    uri,
    server_api=ServerApi('1'),
    tlsCAFile=certifi.where()
)

try:
    # Check the connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def create_session_with_canvases():
    db = client['Uottahack']
    collection = db['sessions']
    
    # Create three sessions
    sessions_data = [
        {
            "session_id": "session1",
            "timestamp": datetime.now(),
            "canvases": [
                {
                    "canvas_id": "canvas1_1",
                    "name": "First Canvas of Session 1",
                    "coordinates": [
                        {'x': 0, 'y': 0, 'z': 0},
                        {'x': 1, 'y': 1, 'z': 0},
                        {'x': 2, 'y': 0, 'z': 0},
                        {'x': 3, 'y': 2, 'z': 0},
                        {'x': 4, 'y': 1, 'z': 0},
                        {'x': 5, 'y': 3, 'z': 0},
                        {'x': 6, 'y': 2, 'z': 0},
                        {'x': 7, 'y': 4, 'z': 0},
                        {'x': 8, 'y': 3, 'z': 0},
                        {'x': 9, 'y': 5, 'z': 0}
                    ]
                },
                {
                    "canvas_id": "canvas1_2",
                    "name": "Second Canvas of Session 1",
                    "coordinates": [
                        {"x": i*15, "y": i*25, "z": i*35} for i in range(10)
                    ]
                }
            ]
        },
        {
            "session_id": "session2",
            "timestamp": datetime.now(),
            "canvases": [
                {
                    "canvas_id": "canvas2_1",
                    "name": "First Canvas of Session 2",
                    "coordinates": [
                        {"x": i*5, "y": i*15, "z": i*25} for i in range(10)
                    ]
                },
                {
                    "canvas_id": "canvas2_2",
                    "name": "Second Canvas of Session 2",
                    "coordinates": [
                        {"x": i*8, "y": i*18, "z": i*28} for i in range(10)
                    ]
                }
            ]
        },
        {
            "session_id": "session3",
            "timestamp": datetime.now(),
            "canvases": [
                {
                    "canvas_id": "canvas3_1",
                    "name": "First Canvas of Session 3",
                    "coordinates": [
                        {"x": i*12, "y": i*22, "z": i*32} for i in range(10)
                    ]
                },
                {
                    "canvas_id": "canvas3_2",
                    "name": "Second Canvas of Session 3",
                    "coordinates": [
                        {"x": i*7, "y": i*17, "z": i*27} for i in range(10)
                    ]
                }
            ]
        }
    ]
    
    # Insert the sessions into the database
    result = collection.insert_many(sessions_data)
    print(f"Inserted {len(result.inserted_ids)} sessions")

# Function to retrieve all sessions
def get_all_sessions():
    db = client['Uottahack']
    collection = db['sessions']
    return list(collection.find())

# Create the sessions with their canvases and coordinates
create_session_with_canvases()

# Retrieve and print the sessions to verify
sessions = get_all_sessions()
for session in sessions:
    print(f"\nSession ID: {session['session_id']}")
    for canvas in session['canvases']:
        print(f"\tCanvas ID: {canvas['canvas_id']}")
        print(f"\tNumber of coordinates: {len(canvas['coordinates'])}")
