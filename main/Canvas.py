import tkinter as tk
from tkinter import ttk
import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from plotter import Plotter

class SessionViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Session and Canvas Viewer")
        self.geometry("400x300")
        self.configure(bg='#f0f0f0')  # Light gray background

        # MongoDB connection setup
        load_dotenv()
        self.client = MongoClient(
            os.getenv("uri"),
            server_api=ServerApi('1'),
            tlsCAFile=certifi.where()
        )
        self.db = self.client['Uottahack']
        self.collection = self.db['sessions']

        # Create and setup the main frame
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 12))

        # Create GUI elements
        self.create_widgets()
        
        # Load initial data
        self.load_sessions()

    def create_widgets(self):
        # Session Selection
        self.session_label = ttk.Label(
            self.main_frame, 
            text="Pick a Session to Display :", 
            style='Title.TLabel'
        )
        self.session_label.pack(pady=(0, 5))

        self.session_var = tk.StringVar()
        self.session_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.session_var,
            state='readonly',
            width=30
        )
        self.session_dropdown.pack(pady=(0, 20))
        self.session_dropdown.bind('<<ComboboxSelected>>', self.on_session_select)

        # Canvas Selection (initially hidden)
        self.canvas_label = ttk.Label(
            self.main_frame, 
            text="Select a Canvas to Display:", 
            style='Title.TLabel'
        )
        self.canvas_var = tk.StringVar()
        self.canvas_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.canvas_var,
            state='readonly',
            width=30
        )
        self.canvas_dropdown.bind('<<ComboboxSelected>>', self.on_canvas_select)
        
        # Don't pack canvas elements initially
        # They will be packed when a session is selected

    def load_sessions(self):
        # Get all sessions from MongoDB
        sessions = list(self.collection.find())
        
        # Create new user-friendly names
        session_names = []
        
        # Prepare a dict to map the 'Session X' name to the actual session data
        self.sessions_data = {}

        for i, session in enumerate(sessions, start=1):
            # Build a new name for each session
            session_name = f"Session {i}"
            session_names.append(session_name)
            
            # Store session data keyed by the new name
            self.sessions_data[session_name] = session
        
        # Update the dropdown with the new session names
        self.session_dropdown['values'] = session_names

    def on_session_select(self, event):
        selected_session = self.session_var.get()
        if selected_session:
            session_data = self.sessions_data[selected_session]
            
            # Create a list of "Canvas 1", "Canvas 2", etc.
            canvas_display_names = [f"Canvas {i+1}" for i in range(len(session_data['canvases']))]
            
            # Show canvas selection elements
            self.canvas_label.pack(pady=(0, 5))
            self.canvas_dropdown.pack(pady=(0, 20))
            
            # Set the display names in the dropdown
            self.canvas_dropdown['values'] = canvas_display_names
            self.canvas_var.set('')

            # Store the mapping between display names and canvas IDs for later use
            # self.canvas_mapping = dict(zip(canvas_display_names, 
            #                             [canvas['canvas_id'] for canvas in session_data['canvases']]))
            

    def on_canvas_select(self, event):
        selected_session = self.session_var.get()
        selected_canvas_display = self.canvas_var.get()  # This is "Canvas 1", "Canvas 2", etc.

        plotter = Plotter(max_points=1000)

        if selected_session and selected_canvas_display:
            # Get the session data
            session_data = self.sessions_data[selected_session]
            
            # Get the index from the display name (subtract 1 because Canvas 1 corresponds to index 0)
            canvas_index = int(selected_canvas_display.split()[1]) - 1
            
            # Get the canvas data using the index
            canvas_data = session_data['canvases'][canvas_index]
            
            if canvas_data:
                coordinates = canvas_data['coordinates']
                print("Coordinates: ")
                print(list(coordinates))

                plotter.add_points(coordinates)
                plotter.start_animation(interval=100)



def main():
        app = SessionViewer()
        app.mainloop()


main()