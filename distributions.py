"""
Author: Catelynn Barfell
Date: 12/03/2024
Short Desc: Distributions Module
Handles the logic for logging and managing distributions.
"""

from database import connect_db

class Distributions:
    @staticmethod
    def log_distribution(name, quantity, recipient):
        """
        Log a distribution to the database.

        Args:
            name (str): Name of the distributed item.
            quantity (int): Quantity distributed.
            recipient (str): Recipient of the distribution.
        """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO distributions (name, quantity, distribution_date, recipient)
            VALUES (?, ?, date('now'), ?)
        """, (name, quantity, recipient))
        conn.commit()
        conn.close()