from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
import certifi
import configparser
from datetime import datetime
from bson import ObjectId

class MongoDBHandler:
    def __init__(self, config_path='config.properties'):
        self.config = self._load_config(config_path)
        self.client = self._setup_client()
        self.db = self.client['Uottahack']
        self.collection = self.db['sessions']
        self.current_session_id = None
        self.current_canvas_id = None
        self._create_new_session()

    def _load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return {
            'username': config.get('mongo', 'username'),
            'password': urllib.parse.quote_plus(config.get('mongo', 'password'))
        }

    def _setup_client(self):
        uri = f"mongodb+srv://{self.config['username']}:{self.config['password']}@digipencluster.laanv.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
        return MongoClient(
            uri,
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where()
        )

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return False

    def _create_new_session(self):
        """Create a new session and initialize first canvas"""
        try:
            session_doc = {
                "timestamp": datetime.now(),
                "canvases": []
            }
            result = self.collection.insert_one(session_doc)
            self.current_session_id = result.inserted_id
            self._create_new_canvas()
            print(f"New session created with ID: {self.current_session_id}")
        except Exception as e:
            print(f"Error creating new session: {e}")

    def _create_new_canvas(self):
        """Create a new canvas in the current session"""
        try:
            canvas = {
                "timestamp": datetime.now(),
                "coordinates": []
            }
            
            result = self.collection.update_one(
                {"_id": self.current_session_id},
                {"$push": {"canvases": canvas}}
            )
            
            # Get the index of the newly created canvas
            session = self.collection.find_one({"_id": self.current_session_id})
            self.current_canvas_id = len(session["canvases"]) - 1
            
            print(f"New canvas created with index: {self.current_canvas_id}")
        except Exception as e:
            print(f"Error creating new canvas: {e}")

    def insert_coordinates(self, x, y, z, timestamp):
        """Insert coordinates and timestamp into the collection"""
        try:
            coordinate_data = {
                "x": x,
                "y": y,
                "z": z,
                "timestamp": timestamp
            }
            result = self.collection.insert_one(coordinate_data)
            print(f"Data inserted with record id {result.inserted_id}")
            return True
        except Exception as e:
            print(f"Error inserting data to MongoDB: {e}")
            return False

    def get_current_session(self):
        """Retrieve the current session data"""
        try:
            return self.collection.find_one({"_id": self.current_session_id})
        except Exception as e:
            print(f"Error retrieving session: {e}")
            return None

    def get_current_canvas(self):
        """Retrieve the current canvas data"""
        try:
            session = self.get_current_session()
            if session and len(session["canvases"]) > self.current_canvas_id:
                return session["canvases"][self.current_canvas_id]
            return None
        except Exception as e:
            print(f"Error retrieving canvas: {e}")
            return None

    def close_connection(self):
        self.client.close()
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# import urllib.parse
# import certifi
# import configparser

# class MongoDBHandler:
#     def __init__(self, config_path='config.properties'):
#         self.config = self._load_config(config_path)
#         self.client = self._setup_client()
#         self.db = self.client['Uottahack']
#         self.collection = self.db['digiPenDB']

#     def _load_config(self, config_path):
#         config = configparser.ConfigParser()
#         config.read(config_path)
#         return {
#             'username': config.get('mongo', 'username'),
#             'password': urllib.parse.quote_plus(config.get('mongo', 'password'))
#         }

#     def _setup_client(self):
#         uri = f"mongodb+srv://{self.config['username']}:{self.config['password']}@digipencluster.laanv.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
#         return MongoClient(
#             uri,
#             server_api=ServerApi('1'),
#             tlsCAFile=certifi.where()
#         )

#     def test_connection(self):
#         try:
#             self.client.admin.command('ping')
#             print("Successfully connected to MongoDB!")
#             return True
#         except Exception as e:
#             print(f"MongoDB connection error: {e}")
#             return False

#     def insert_coordinates(self, x, y, z, timestamp):
#         try:
#             coordinate_data = {
#                 "x": x,
#                 "y": y,
#                 "z": z,
#                 "timestamp": timestamp
#             }
#             result = self.collection.insert_one(coordinate_data)
#             print(f"Data inserted with record id {result.inserted_id}")
#             return True
#         except Exception as e:
#             print(f"Error inserting data to MongoDB: {e}")
#             return False

#     def close_connection(self):
#         self.client.close()