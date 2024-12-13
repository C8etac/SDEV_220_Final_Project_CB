"""
Author: Catelynn Barfell
Date: 12/03/2024
Assignment: Module 8 Final Project
Short Desc: GUI Module
This module manages the graphical user interface (GUI) for the BC Food Pantry system.

Classes:
- `FoodPantryApp`: Main application class for managing the GUI tabs and widgets.

Functions:
- `__init__`: Initializes the GUI application.
- `setup_tabs`: Creates tabs for Inventory, Donations, Distributions, and Recipients.
- `schedule_real_time_updates`: Schedules periodic updates for inventory and recipient dropdowns.
- `setup_inventory_tab`: Sets up the Inventory management tab.
- `setup_recipients_tab`: Sets up the Recipients management tab.
- `update_item_dropdown`: Updates the inventory item dropdown in real-time.
- `update_recipient_dropdown`: Updates the recipient dropdown in real-time.
- `check_notifications`: Checks and displays notifications for low stock or expiring items.
- `load_inventory`: Loads and displays inventory data in the Inventory tab.
- `add_inventory_item`: Handles adding a new item to the inventory.
- `add_recipient_window`: Handles adding a new recipient to the Recipients tab.
- `load_recipients`: Loads and displays recipients in the Recipients tab.
- `remove_recipient`: Removes a selected recipient from the Recipients tab.
- `remove_inventory_item`: Removes a selected item from the Inventory tab.
- `setup_donation_tab`: Sets up the Donations management tab.
- `setup_distribution_tab`: Sets up the Distributions management tab.
- `log_donation`: Logs a new donation and updates inventory.
- `log_distribution`: Logs a new distribution and updates inventory.

Dependencies:
- `tkinter`
- `Inventory`
- `Notifications`
- `Donations`
- `Distributions`
- `Recipients`
"""

import tkinter as tk
from tkinter import ttk, messagebox
from inventory import Inventory
from notifications import Notifications
from donations import Donations
from distributions import Distributions
from recipients import Recipients


# Main application class for the food pantry system.
class FoodPantryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BC Food Pantry System")

        # Setup tabs for the GUI
        self.setup_tabs()
        self.check_notifications()

    # Create tabs for inventory, donations, and distributions.
    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Inventory Tab
        self.inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")
        self.setup_inventory_tab()

        # Donations Tab
        self.donation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.donation_tab, text="Donations")
        self.setup_donation_tab()

        # Distribution Tab
        self.distribution_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.distribution_tab, text="Distributions")
        self.setup_distribution_tab()

        # Recipients Tab
        self.recipients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.recipients_tab, text="Recipients")
        self.setup_recipients_tab()
        
        # Schedule periodic updates
        self.schedule_real_time_updates()

    # Schedule real-time updates for the distribution tab.
    def schedule_real_time_updates(self):        
        self.update_item_dropdown()
        self.root.after(5000, self.schedule_real_time_updates)    

    def setup_inventory_tab(self):
        ttk.Label(self.inventory_tab, text="Manage Inventory").pack()

        # Table to display inventory
        self.inventory_tree = ttk.Treeview(
            self.inventory_tab, columns=("name", "type", "quantity", "expiration"), show="headings"
        )
        self.inventory_tree.heading("name", text="Name")
        self.inventory_tree.heading("type", text="Type")
        self.inventory_tree.heading("quantity", text="Quantity")
        self.inventory_tree.heading("expiration", text="Expiration Date")
        self.inventory_tree.pack()

        # Buttons for managing inventory
        ttk.Button(self.inventory_tab, text="Add Item", command=self.add_inventory_item).pack()
        ttk.Button(self.inventory_tab, text="Remove Item", command=self.remove_inventory_item).pack()
        ttk.Button(self.inventory_tab, text="Check Notifications", command=self.check_notifications).pack()
        ttk.Button(self.inventory_tab, text="Refresh", command=self.load_inventory).pack()

        self.load_inventory()

    # Set up the Recipients tab.
    def setup_recipients_tab(self):
        ttk.Label(self.recipients_tab, text="Manage Recipients").pack()

        # Table to display recipients
        self.recipients_tree = ttk.Treeview(
            self.recipients_tab, columns=("id", "name", "contact", "address"), show="headings"
        )
        self.recipients_tree.heading("id", text="ID")
        self.recipients_tree.heading("name", text="Name")
        self.recipients_tree.heading("contact", text="Contact")
        self.recipients_tree.heading("address", text="Address")
        self.recipients_tree.pack()

        # Buttons for managing recipients
        ttk.Button(self.recipients_tab, text="Add Recipient", command=self.add_recipient_window).pack()
        ttk.Button(self.recipients_tab, text="Remove Recipient", command=self.remove_recipient).pack()
        ttk.Button(self.recipients_tab, text="Refresh", command=self.load_recipients).pack()

        self.load_recipients()
    
    # Update the dropdown menu with current inventory items.
    def update_item_dropdown(self):
        try:
            # Fetch current inventory items
            items = [row[0] for row in Inventory.load_items()]
            self.item_dropdown["values"] = items
            if items:
                self.item_dropdown.current(0)
            else:
                self.item_dropdown.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item dropdown: {e}")

    # Check for low stock and items expiring within 7 days.
    def check_notifications(self):
        try:
            # Fetch low stock items
            low_stock_items = Notifications.get_low_stock_items()
            expiring_items = Notifications.get_expiring_items_within(7)

            # Prepare notification messages
            messages = []

            if low_stock_items:
                low_stock_message = "\n".join(f"{item[0]} has only {item[1]} left" for item in low_stock_items)
                messages.append(f"Low Stock Items:\n{low_stock_message}")

            if expiring_items:
                expiring_message = "\n".join(f"{item[0]} expires on {item[1]}" for item in expiring_items)
                messages.append(f"Expiring Items (Next 7 Days):\n{expiring_message}")

            # Show notifications if any
            if messages:
                messagebox.showinfo("Notifications", "\n\n".join(messages))
            else:
                messagebox.showinfo("Notifications", "No notifications at this time.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check notifications: {e}")

    # Load inventory data into the table.
    def load_inventory(self):
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        for row in Inventory.load_items():
            self.inventory_tree.insert("", "end", values=row)

    # Logic for opening the add item window
    def add_inventory_item(self):
        add_item_window = tk.Toplevel(self.root)
        add_item_window.title("Add Inventory Item")
        add_item_window.geometry("400x300")

        # Labels and entry fields
        ttk.Label(add_item_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        item_name = tk.StringVar()
        ttk.Entry(add_item_window, textvariable=item_name).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(add_item_window, text="Type:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        item_type = tk.StringVar()
        type_dropdown = ttk.Combobox(
            add_item_window, textvariable=item_type, state="readonly"
        )
        type_dropdown["values"] = ("Perishable", "Non-Perishable")
        type_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        type_dropdown.current(0)  

        ttk.Label(add_item_window, text="Quantity:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        item_quantity = tk.IntVar()
        ttk.Entry(add_item_window, textvariable=item_quantity).grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(add_item_window, text="Expiration Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        item_expiration = tk.StringVar()
        ttk.Entry(add_item_window, textvariable=item_expiration).grid(row=3, column=1, padx=10, pady=10)

        # Add Item Button
        def save_item():
            name = item_name.get()
            type_ = item_type.get()
            quantity = item_quantity.get()
            expiration = item_expiration.get()

            if name and type_ and quantity and expiration:
                try:
                    Inventory.add_item(name, type_, quantity, expiration)
                    messagebox.showinfo("Success", "Item added successfully!")
                    self.load_inventory() 
                    add_item_window.destroy() 
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add item: {e}")
            else:
                messagebox.showerror("Error", "All fields are required.")

        ttk.Button(add_item_window, text="Add Item", command=save_item).grid(row=4, column=0, columnspan=2, pady=20)

    # Window to add a new recipient.
    def add_recipient_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Recipient")
        window.geometry("400x400")

        # Recipient Name
        ttk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name = tk.StringVar()
        ttk.Entry(window, textvariable=name).grid(row=0, column=1, padx=10, pady=10)

        # Phone Number
        ttk.Label(window, text="Phone (###) ###-####:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        phone = tk.StringVar()
        phone_entry = ttk.Entry(window, textvariable=phone)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)

        # Street Address
        ttk.Label(window, text="Street Address:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        street_address = tk.StringVar()
        ttk.Entry(window, textvariable=street_address).grid(row=2, column=1, padx=10, pady=10)

        # City
        ttk.Label(window, text="City:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        city = tk.StringVar()
        ttk.Entry(window, textvariable=city).grid(row=3, column=1, padx=10, pady=10)

        # State
        ttk.Label(window, text="State:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        state = tk.StringVar()
        ttk.Entry(window, textvariable=state).grid(row=4, column=1, padx=10, pady=10)

        # Zipcode
        ttk.Label(window, text="Zipcode:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        zipcode = tk.StringVar()
        ttk.Entry(window, textvariable=zipcode).grid(row=5, column=1, padx=10, pady=10)

        # Save the recipient to the database.
        def save_recipient():
            if name.get() and phone.get() and street_address.get() and city.get() and state.get() and zipcode.get():
                try:
                    address = f"{street_address.get()}, {city.get()}, {state.get()} {zipcode.get()}"
                    Recipients.add_recipient(name.get(), phone.get(), address)
                    messagebox.showinfo("Success", "Recipient added successfully!")
                    self.load_recipients() 
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add recipient: {e}")
            else:
                messagebox.showerror("Error", "All fields are required.")

        ttk.Button(window, text="Save", command=save_recipient).grid(row=6, column=0, columnspan=2, pady=20)

    # Load all recipients into the table.
    def load_recipients(self):
        self.recipients_tree.delete(*self.recipients_tree.get_children())
        for row in Recipients.load_recipients():
            self.recipients_tree.insert("", "end", values=row)

    # Remove the selected recipient.
    def remove_recipient(self):
        selected_item = self.recipients_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a recipient to remove.")
            return

        recipient_id = self.recipients_tree.item(selected_item, "values")[0] 
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove this recipient?")
        if confirm:
            try:
                Recipients.remove_recipient(recipient_id)
                self.load_recipients()
                messagebox.showinfo("Success", "Recipient removed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove recipient: {e}")

    # Remove the selected item from inventory.
    def remove_inventory_item(self):
        selected_item = self.inventory_tree.selection() 

        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove.")
            return

        # Get the item's name
        item_name = self.inventory_tree.item(selected_item, "values")[0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{item_name}'?")
        if not confirm:
            return

        # Remove item from the database
        try:
            Inventory.remove_item(item_name)  
            self.load_inventory() 
            messagebox.showinfo("Success", f"Item '{item_name}' removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove item: {e}")

    # Setup the donations management tab.
    def setup_donation_tab(self):
        ttk.Label(self.donation_tab, text="Log Donations").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(self.donation_tab, text="Name:").grid(row=1, column=0, sticky="e")
        self.donation_name = tk.StringVar()
        ttk.Entry(self.donation_tab, textvariable=self.donation_name).grid(row=1, column=1, sticky="w")

        ttk.Label(self.donation_tab, text="Type:").grid(row=2, column=0, sticky="e")
        self.donation_type = tk.StringVar() 
        self.type_dropdown = ttk.Combobox(
            self.donation_tab, textvariable=self.donation_type, state="readonly"
        )
        self.type_dropdown["values"] = ("Perishable", "Non-Perishable")
        self.type_dropdown.grid(row=2, column=1, sticky="w")
        self.type_dropdown.current(0) 

        ttk.Label(self.donation_tab, text="Quantity:").grid(row=3, column=0, sticky="e")
        self.donation_quantity = tk.IntVar()
        ttk.Entry(self.donation_tab, textvariable=self.donation_quantity).grid(row=3, column=1, sticky="w")

        ttk.Label(self.donation_tab, text="Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e")
        self.donation_date = tk.StringVar()
        ttk.Entry(self.donation_tab, textvariable=self.donation_date).grid(row=4, column=1, sticky="w")

        ttk.Button(self.donation_tab, text="Log Donation", command=self.log_donation).grid(row=5, column=0, columnspan=2, pady=5)

    # Setup the distributions management tab.
    def setup_distribution_tab(self):
        ttk.Label(self.distribution_tab, text="Distribute Items").grid(row=0, column=0, columnspan=2, pady=5)

        # Item Name Dropdown
        ttk.Label(self.distribution_tab, text="Item Name:").grid(row=1, column=0, sticky="e")
        self.distribution_item = tk.StringVar()
        self.item_dropdown = ttk.Combobox(
            self.distribution_tab, textvariable=self.distribution_item, state="readonly"
        )
        self.item_dropdown.grid(row=1, column=1, sticky="w")
        self.update_item_dropdown() 

        # Recipient Dropdown
        ttk.Label(self.distribution_tab, text="Recipient:").grid(row=2, column=0, sticky="e")
        self.distribution_recipient = tk.StringVar()
        self.recipient_dropdown = ttk.Combobox(
            self.distribution_tab, textvariable=self.distribution_recipient, state="readonly"
        )
        self.recipient_dropdown.grid(row=2, column=1, sticky="w")
        self.update_recipient_dropdown() 

        # Quantity
        ttk.Label(self.distribution_tab, text="Quantity:").grid(row=3, column=0, sticky="e")
        self.distribution_quantity = tk.IntVar()
        ttk.Entry(self.distribution_tab, textvariable=self.distribution_quantity).grid(row=3, column=1, sticky="w")

        ttk.Button(self.distribution_tab, text="Distribute", command=self.log_distribution).grid(row=4, column=0, columnspan=2, pady=10)

    # Update the recipient dropdown with the current recipients.
    def update_recipient_dropdown(self):
        try:
            # Fetch current recipients
            recipients = [row[1] for row in Recipients.load_recipients()]
            self.recipient_dropdown["values"] = recipients
            if recipients:
                self.recipient_dropdown.current(0)
            else:
                self.recipient_dropdown.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update recipient dropdown: {e}")

    # Logic for logging donations.
    def log_donation(self):
        name = self.donation_name.get()
        type_ = self.donation_type.get()
        quantity = self.donation_quantity.get()
        donation_date = self.donation_date.get()

        if name and type_ and quantity and donation_date:
            try:
                # Log the donation
                Donations.log_donation(name, type_, quantity, donation_date)

                # Add to inventory
                Inventory.add_item(name, type_, quantity, donation_date)

                # Success
                messagebox.showinfo("Success", "Donation logged and added to inventory successfully!")
                self.load_inventory() 
                self.update_item_dropdown()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log donation: {e}")
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Log a distribution and update inventory.
    def log_distribution(self):
        item_name = self.distribution_item.get()
        quantity = self.distribution_quantity.get()
        recipient = self.distribution_recipient.get()

        if not item_name or not quantity or not recipient:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Check current inventory
            current_item = next((item for item in Inventory.load_items() if item[0] == item_name), None)
            if not current_item:
                messagebox.showerror("Error", "Item not found in inventory.")
                return

            current_quantity = current_item[2]
            if quantity > current_quantity:
                messagebox.showerror("Error", "Insufficient inventory for distribution.")
                return

            # Deduct from inventory
            Inventory.update_quantity(item_name, current_quantity - quantity)

            # Log the distribution
            Distributions.log_distribution(item_name, quantity, recipient)

            # Success
            messagebox.showinfo("Success", "Distribution logged and inventory updated.")
            self.load_inventory() 
            self.update_item_dropdown()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log distribution: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodPantryApp(root)
    root.mainloop()