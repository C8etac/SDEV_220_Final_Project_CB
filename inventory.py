"""
Author: Catelynn Barfell
Date: 12/08/2024
Assignment: Module 8 Final Project
Short Desc:

"""

from database import connect_db

class Inventory:
    # Load items in the inventory
    @staticmethod
    def load_items():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, type, quantity, expiration_date FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        return rows

    # Add an item to the inventory
    @staticmethod
    def add_item(name, type_, quantity, expiration_date):
        """    
        Args:
            name (str): Name of the item.
            type_ (str): Type of the item (Perishable/Non-Perishable).
            quantity (int): Quantity of the item.
            expiration_date (str): Expiration date of the item.
        """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventory (name, type, quantity, expiration_date)
            VALUES (?, ?, ?, ?)
        """, (name, type_, quantity, expiration_date))
        conn.commit()
        conn.close()

    # Update stock of item in the inventory 
    @staticmethod
    def update_stock(name, quantity):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE name = ?",
            (quantity, name)
        )
        conn.commit()
        conn.close()

    # Remove item from the inventory
    @staticmethod
    def remove_item(name):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM inventory WHERE name = ?", 
            (name,)
        )
        conn.commit()
        conn.close()

    # Update quantity of an item in the inventory
    @staticmethod
    def update_quantity(name, quantity):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE name = ?", 
            (quantity, name)
        )
        conn.commit()
        conn.close()