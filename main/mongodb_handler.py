from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
import certifi
import configparser

class MongoDBHandler:
    def __init__(self, config_path='config.properties'):
        self.config = self._load_config(config_path)
        self.client = self._setup_client()
        self.db = self.client['Uottahack']
        self.collection = self.db['digiPenDB']

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

    def insert_coordinates(self, x, y, z):
        try:
            coordinate_data = {
                "x": x,
                "y": y,
                "z": z
            }
            result = self.collection.insert_one(coordinate_data)
            print(f"Data inserted with record id {result.inserted_id}")
            return True
        except Exception as e:
            print(f"Error inserting data to MongoDB: {e}")
            return False

    def close_connection(self):
        self.client.close()