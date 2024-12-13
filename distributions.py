"""
Author: Catelynn Barfell
Date: 12/03/2024
Assignment: Module 8 Final Project
Short Desc: Distributions Module
This module manages the logic for logging and managing item distributions in the BC Food Pantry system.

Class:
- `Distributions`: Contains static methods to handle distribution operations.

Functions:
- `log_distribution()`: Logs a distribution entry in the database.
"""

from database import connect_db

# Logs a distribution to the database.
class Distributions:
    @staticmethod
    def log_distribution(name, quantity, recipient):
        if not name or not recipient:
            raise ValueError("Name and recipient cannot be empty.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO distributions (name, quantity, distribution_date, recipient)
                VALUES (?, ?, date('now'), ?)
            """, (name, quantity, recipient))
            conn.commit()
        except Exception as e:
            print(f"Error logging distribution: {e}")
            raise
        finally:
            if conn:
                conn.close()