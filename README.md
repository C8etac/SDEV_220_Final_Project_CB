
BC Food Pantry System
Overview
The BC Food Pantry System is a comprehensive inventory and resource management application tailored for food pantries. This system allows users to manage inventory, donations, distributions, and recipients efficiently with a user-friendly graphical interface built using Python's tkinter.

Features

Inventory Management
Add, remove, and view items in the pantry's inventory.
Track item types (perishable or non-perishable), quantities, and expiration dates.
Notifications for low-stock items or items expiring within the next 7 days.

Donations Management
Log donations with details such as item name, type, quantity, and donation date.
Automatically updates inventory with new donations.

Distributions Management
Log distributions of inventory items to recipients.
Automatically deducts distributed quantities from inventory.
Allows selection of recipients from a dropdown list.

Recipient Management
Add, remove, and view recipients.
Store detailed recipient information, including:
 - Name
 - Contact (formatted as (###) ###-####)
 - Address (street, city, state, ZIP code)
Recipients are dynamically integrated into the distribution system.

Notifications
Real-time notifications for:
 - Items expiring within 7 days.
 - Low-stock items (threshold configurable).
Customizable notification intervals.


Installation Requirements
Python 3.8 or higher
SQLite
Required Python libraries:
 - tkinter
 - sqlite3


Usage
Start the Application: Launch the GUI by running main.py.
Manage Inventory: Navigate to the Inventory tab to add or remove items, refresh the list, and check notifications.
Log Donations: Use the Donations tab to log new donations, automatically updating the inventory.
Log Distributions: Distribute items from inventory to recipients via the Distributions tab.
Manage Recipients: Add or remove recipients in the Recipients tab. Recipients are used in the distribution process.