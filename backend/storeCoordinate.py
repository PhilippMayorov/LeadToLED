from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
import certifi

# Encode the password to handle special characters
password = urllib.parse.quote_plus("digiPenPassword")
username = "philipp"

# Connection URI
uri = f"mongodb+srv://{username}:{password}@digipencluster.laanv.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

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

# Function to insert coordinates
def insert_coordinates(x, y, z):
    # Choose your database
    db = client['Uottahack']  # Replace 'mydatabase' with your database name
    # Choose the collection
    collection = db['digiPenDB']  # Replace 'coordinates' with your collection name

    # Coordinate data to be inserted
    coordinate_data = {
        "x": x,
        "y": y,
        "z": z
    }
    
    # Inserting the data into the collection
    result = collection.insert_one(coordinate_data)
    print("Data inserted with record id", result.inserted_id)

# Example usage of the function
insert_coordinates(1, 2, 3)
insert_coordinates(4, 5, 70)
insert_coordinates(500, 600, 700)
insert_coordinates(5000, 6000, 7000)
insert_coordinates(50000, 60000, 70000)

