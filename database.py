"""
Author: Catelynn Barfell
Date: 12/03/2024
Assignment: Module 8 Final Project
Short Desc: Database Module
Handles all database-related operations, including setup and connections.
Functions:
- `connect_db()`: Establishes a connection to the SQLite database.
- `setup_database()`: Creates tables for inventory, donations, and distributions.
"""

import sqlite3

# Establish and return a connection to the SQLite database.
def connect_db():
    """
    Establishes and returns a connection to the SQLite database.
    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    try:
        conn = sqlite3.connect("food_pantry.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

# Create or update tables if they do not exist.
def setup_database():
    """
    Sets up the SQLite database by creating or updating tables as needed.
    Creates the `inventory`, `donations`, and `distributions` tables if they do not exist.
    """
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Create `inventory` table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                expiration_date TEXT
            )
        """)

        # Create `donations` table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                donation_date TEXT NOT NULL
            )
        """)

        # Create `distributions` table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS distributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                distribution_date TEXT NOT NULL,
                recipient TEXT NOT NULL
            )
        """)
        
        # Create recipients table with phone number
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                address TEXT
            )
        """)

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        raise
    finally:
        if conn:
            conn.close()