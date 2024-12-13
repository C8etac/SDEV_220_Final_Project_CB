"""
Author: Catelynn Barfell
Date: 12/03/2024
Assignment: Module 8 Final Project
Short Desc: Main Application File
This file initializes the system, sets up the database, and launches the GUI.
Modules:
- `database.py` for database setup.
- `gui.py` for the graphical interface.

"""
from database import setup_database
import tkinter as tk
from gui import FoodPantryApp

# Ensure database is ready before starting GUI
if __name__ == "__main__":
    setup_database()
    
    # Initialize the GUI
    root = tk.Tk()
    app = FoodPantryApp(root)
    root.mainloop()