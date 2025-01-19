import tkinter as tk
from tkinter import ttk
import os
import urllib.parse
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
        session_ids = [session['session_id'] for session in sessions]
        self.session_dropdown['values'] = session_ids
        
        # Store sessions data for later use
        self.sessions_data = {session['session_id']: session for session in sessions}

    def on_session_select(self, event):
        selected_session = self.session_var.get()
        if selected_session:
            session_data = self.sessions_data[selected_session]
            canvas_ids = [canvas['canvas_id'] for canvas in session_data['canvases']]
            
            # Show canvas selection elements
            self.canvas_label.pack(pady=(0, 5))
            self.canvas_dropdown.pack(pady=(0, 20))
            
            self.canvas_dropdown['values'] = canvas_ids
            self.canvas_var.set('')  # Reset canvas selection

    def on_canvas_select(self, event):
        selected_session = self.session_var.get()
        selected_canvas = self.canvas_var.get()

        plotter = Plotter(max_points=1000)

        if selected_session and selected_canvas:
            session_data = self.sessions_data[selected_session]
            canvas_data = next(
                (canvas for canvas in session_data['canvases'] 
                    if canvas['canvas_id'] == selected_canvas), 
                None
            )
            
            if canvas_data:
                coordinates = canvas_data['coordinates']
                plotter.add_points(coordinates)
                plotter.start_animation(interval=100)


def main():
        app = SessionViewer()
        app.mainloop()


main()