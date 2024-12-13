"""
Author: Catelynn Barfell
Date: 12/08/2024
Assignment: Module 8 Final Project
Short Desc:

"""

from database import connect_db

class Recipients:
    
    # Add a new recipient to the database.
    @staticmethod
    def add_recipient(name, contact, address):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipients (name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
        conn.commit()
        conn.close()

    # Load all recipients from the database.
    @staticmethod
    def load_recipients():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, contact, address FROM recipients")
        recipients = cursor.fetchall()
        conn.close()
        return recipients

    # Remove a recipient from the database.
    @staticmethod
    def remove_recipient(recipient_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipients WHERE id = ?", (recipient_id,))
        conn.commit()
        conn.close()