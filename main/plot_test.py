# test_plotter.py
from plotter import Plotter

def test_simple_points():

    plotter = Plotter(max_points=1000)
    
    # Simple array of coordinates
    coordinates = [
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
    
    # Add points to plotter
    plotter.add_points(coordinates)
    
    # Start animation
    plotter.start_animation(interval=100)  # 500ms between points

if __name__ == "__main__":
    test_simple_points()