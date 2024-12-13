"""
Author: Catelynn Barfell
Date: 12/12/2024
Assignment: Module 8 Final Project
Short Desc: Testing File
This file tests all the features of the BC Food Pantry system, ensuring functionality across all modules.

Modules Tested:
- `database`
- `inventory`
- `notifications`
- `donations`
- `distributions`
- `recipients`

"""


import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from database import setup_database, connect_db
from inventory import Inventory
from donations import Donations
from distributions import Distributions
from notifications import Notifications
from recipients import Recipients

print("Test file is running")

class TestFoodPantrySystem(unittest.TestCase):

    # Setup the database and populate initial data.
    @classmethod
    def setUpClass(cls):        
        setup_database()
        Inventory.add_item("Apples", "Perishable", 50, "2024-12-31")
        Inventory.add_item("Rice", "Non-Perishable", 100, None)
        Recipients.add_recipient("John Doe", "(123) 456-7890", "123 Elm St, City, State 12345")
        Donations.log_donation("Canned Beans", "Non-Perishable", 30, "2024-12-10")

    # Clean up the database after all tests.
    @classmethod
    def tearDownClass(cls):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM donations")
        cursor.execute("DELETE FROM distributions")
        cursor.execute("DELETE FROM recipients")
        conn.commit()
        conn.close()

    # Test loading inventory items.
    def test_inventory_load(self):
        items = Inventory.load_items()
        self.assertGreater(len(items), 0)
        self.assertIn(("Apples", "Perishable", 50, "2024-12-31"), items)
        print("test_inventory_load passed")

    # Test adding an inventory item.
    def test_add_inventory_item(self):
        Inventory.add_item("Milk", "Perishable", 20, "2024-12-15")
        items = Inventory.load_items()
        self.assertIn(("Milk", "Perishable", 20, "2024-12-15"), items)
        print("test_add_inventory_item passed")

    # Test removing an inventory item.
    def test_remove_inventory_item(self):
        Inventory.remove_item("Apples")
        items = Inventory.load_items()
        self.assertNotIn(("Apples", "Perishable", 50, "2024-12-31"), items)
        print("test_remove_inventory_item passed")

    # Test logging a donation.
    def test_log_donation(self):
        Donations.log_donation("Bread", "Perishable", 10, "2024-12-11")
        donations = Donations.get_donations()
        self.assertIn(("Bread", 10, "2024-12-11"), donations)
        print("test_log_donation passed")

    # Test logging a distribution.
    def test_log_distribution(self):
        Distributions.log_distribution("Rice", 10, "John Doe")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, recipient FROM distributions")
        distributions = cursor.fetchall()
        conn.close()
        self.assertIn(("Rice", 10, "John Doe"), distributions)
        print("test_log_distribution passed")

    # Test fetching low stock notifications.
    def test_low_stock_notification(self):
        Inventory.update_stock("Rice", 5)
        low_stock = Notifications.get_low_stock_items()
        self.assertIn(("Rice", 5), low_stock)
        print("test_low_stock_notification passed")

    # Test fetching expiring items notification.
    def test_expiring_items_notification(self):
        expiring_items = Notifications.get_expiring_items_within(30)
        self.assertIn(("Milk", "2024-12-15"), expiring_items)
        print("test_expiring_items_notification passed")

    # Test adding a recipient.
    def test_add_recipient(self):
        Recipients.add_recipient("Jane Smith", "(987) 654-3210", "456 Oak St, City, State 54321")
        recipients = Recipients.load_recipients()
        added_recipient = next(
            (recipient for recipient in recipients if recipient[1] == "Jane Smith"), None
        )

        self.assertIsNotNone(added_recipient)
        self.assertEqual(added_recipient[1:], ("Jane Smith", "(987) 654-3210", "456 Oak St, City, State 54321"))
        print("test_add_recipient passed")

    # Test removing a recipient.
    def test_remove_recipient(self):
        recipients = Recipients.load_recipients()
        recipient_id = recipients[0][0]  # Get the ID of the first recipient
        Recipients.remove_recipient(recipient_id)
        updated_recipients = Recipients.load_recipients()
        self.assertNotIn((recipient_id, "John Doe", "(123) 456-7890", "123 Elm St, City, State 12345"), updated_recipients)
        print("test_remove_recipient passed")

if __name__ == "__main__":
    unittest.main()
