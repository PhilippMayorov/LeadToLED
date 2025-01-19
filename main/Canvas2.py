from plotter import Plotter
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi

# Load environment variables
load_dotenv()

# Create a MongoDB client
client = MongoClient(
    os.getenv("uri"),
    server_api=ServerApi('1'),
    tlsCAFile=certifi.where()
)

# Select your database
db = client['Uottahack']
# Select your collection
digiPenDB = db['digiPenDB']

# Retrieve all documents from the collection and convert to list
coordinates = list(digiPenDB.find({}, {'_id': 0}))

class CustomPlotter(Plotter):
    def _animate(self, framedata):
          # Debug print to check what framedata contains
        print("Frame data:", framedata)

        # Check if framedata is a dictionary and contains 'x', 'y', 'z'
        if isinstance(framedata, dict) and {'x', 'y', 'z'}.issubset(framedata):
            self.add_point(framedata['x'], framedata['y'], framedata['z'])
        else:
            print("Error: Expected framedata to be a dict with 'x', 'y', 'z' keys")
            print({framedata})
   

def test_simple_points():
    plotter = CustomPlotter()

    print(coordinates)  # Optionally print coordinates to debug
    # Add points to plotter (assuming add_points can accept a list of dicts)
    plotter.add_points(coordinates)
    
    # Start animation
    plotter.start_animation(interval=50)  # 100ms between frames

if __name__ == "__main__":
    test_simple_points()
