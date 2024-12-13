"""
Author: Catelynn Barfell
Date: 12/03/2024
Assignment: Module 8 Final Project
Short Description: 
This module manages all database-related operations for the BC Food Pantry system, including connection establishment and table creation.

Functions:
- `connect_db()`: Establishes a connection to the SQLite database.
- `setup_database()`: Creates or updates tables for inventory, donations, distributions, and recipients.

Database Tables:
1. `inventory`:
    - `id` (INTEGER, PRIMARY KEY): Unique identifier for each inventory item.
    - `name` (TEXT, NOT NULL): Name of the item.
    - `type` (TEXT, NOT NULL): Type of item (e.g., Perishable, Non-Perishable).
    - `quantity` (INTEGER, NOT NULL): Quantity of the item in stock.
    - `expiration_date` (TEXT): Expiration date of the item (if applicable).

2. `donations`:
    - `id` (INTEGER, PRIMARY KEY): Unique identifier for each donation.
    - `name` (TEXT, NOT NULL): Name of the donated item.
    - `type` (TEXT, NOT NULL): Type of item (e.g., Perishable, Non-Perishable).
    - `quantity` (INTEGER, NOT NULL): Quantity of the donated item.
    - `donation_date` (TEXT, NOT NULL): Date the donation was logged.

3. `distributions`:
    - `id` (INTEGER, PRIMARY KEY): Unique identifier for each distribution.
    - `name` (TEXT, NOT NULL): Name of the distributed item.
    - `quantity` (INTEGER, NOT NULL): Quantity of the item distributed.
    - `distribution_date` (TEXT, NOT NULL): Date of distribution.
    - `recipient` (TEXT, NOT NULL): Name of the recipient.

4. `recipients`:
    - `id` (INTEGER, PRIMARY KEY): Unique identifier for each recipient.
    - `name` (TEXT): Name of the recipient.
    - `contact` (TEXT): Phone number of the recipient.
    - `address` (TEXT): Address of the recipient.
"""

import sqlite3

# Establish and return a connection to the SQLite database.
def connect_db():    
    try:
        conn = sqlite3.connect("food_pantry.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

# Create or update tables if they do not exist.
def setup_database():
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