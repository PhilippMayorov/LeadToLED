import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

# MongoDB URI
uri = os.getenv("uri")
client = MongoClient(uri, tlsCAFile=certifi.where())

# Select your database
db = client['Uottahack']
collection = db['digiPenDB'] 

def getCoords(): 
    # Using projection to only return x, y, and z fields
    # 1 means include the field, 0 means exclude
    # _id is included by default unless explicitly excluded
    return list(collection.find({}, {'_id': 0, 'x': 1, 'y': 1, 'z': 1}))

print(getCoords())