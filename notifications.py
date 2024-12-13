"""
Author: Catelynn Barfell
Date: 12/08/2024
Assignment: Module 8 Final Project
Short Desc: Notifications Module
This module handles notifications for low stock and expiring items in the BC Food Pantry system.

Functions:
- `get_low_stock_items`: Retrieves inventory items with quantities below a specified threshold.
- `get_expiring_items_within`: Retrieves inventory items that are expiring within a specified number of days.

Dependencies:
- `connect_db`
- `datetime`
"""

from database import connect_db
from datetime import datetime, timedelta

class Notifications:
    # Inventory items with quantity below the threshold.
    @staticmethod
    def get_low_stock_items(threshold=10):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM inventory WHERE quantity < ?", (threshold,))
        low_stock_items = cursor.fetchall()
        conn.close()
        return low_stock_items

    # Inventory items expiring within the next specified number of days.
    @staticmethod
    def get_expiring_items_within(days):
        conn = connect_db()
        cursor = conn.cursor()

        # Calculate the date range
        today = datetime.today().date()
        end_date = today + timedelta(days=days)

        cursor.execute("""
            SELECT name, expiration_date
            FROM inventory
            WHERE expiration_date BETWEEN ? AND ?
        """, (today.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        expiring_items = cursor.fetchall()
        conn.close()
        return expiring_items