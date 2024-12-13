"""
Author: Catelynn Barfell
Date: 12/10/2024
Assignment: Module 8 Final Project
Short Desc: Donations Module
This module handles all operations related to managing donations in the BC Food Pantry system.

Functions:
- `log_donation`: Logs a donation record into the database.
- `get_donations`: Retrieves all donation records from the database.

Dependencies:
- `connect_db`
"""


from database import connect_db

class Donations:
    # Logs a donation to the database.
    @staticmethod
    def log_donation(name, type_, quantity, donation_date):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (name, type, quantity, donation_date)
            VALUES (?, ?, ?, ?)
        """, (name, type_, quantity, donation_date))
        conn.commit()
        conn.close()

    # Retrieves all donation records from the database.
    @staticmethod
    def get_donations():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, donation_date FROM donations")
        donations = cursor.fetchall()
        conn.close()
        return donations