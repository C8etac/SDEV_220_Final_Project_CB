import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from inventory_management import InventoryManager, FoodItem
from donation_logger import DonationLogger, Donation
from distribution_manager import DistributionManager, DistributionRecord


class FoodPantryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beach Community Food Pantry System")
        self.geometry("700x500")

        # Initialize Managers
        self.inventory_manager = InventoryManager()
        self.donation_logger = DonationLogger()
        self.distribution_manager = DistributionManager()

        # Create Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add Tabs
        self.create_inventory_tab()
        self.create_donation_tab()
        self.create_distribution_tab()

    def create_inventory_tab(self):
        inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(inventory_tab, text="Inventory Management")

        # Inventory Input Fields
        tk.Label(inventory_tab, text="Food Item Name:").pack()
        self.inv_name_entry = tk.Entry(inventory_tab)
        self.inv_name_entry.pack()

        tk.Label(inventory_tab, text="Type (e.g., Non-perishable):").pack()
        self.inv_type_entry = tk.Entry(inventory_tab)
        self.inv_type_entry.pack()

        tk.Label(inventory_tab, text="Quantity:").pack()
        self.inv_quantity_entry = tk.Entry(inventory_tab)
        self.inv_quantity_entry.pack()

        tk.Label(inventory_tab, text="Expiration Date (YYYY-MM-DD):").pack()
        self.inv_expiration_entry = tk.Entry(inventory_tab)
        self.inv_expiration_entry.pack()

        tk.Button(inventory_tab, text="Add Food Item", command=self.add_inventory_item).pack()

        # Inventory List
        self.inventory_listbox = tk.Listbox(inventory_tab, height=10)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True)
        tk.Button(inventory_tab, text="Show Inventory", command=self.show_inventory).pack()

    def create_donation_tab(self):
        donation_tab = ttk.Frame(self.notebook)
        self.notebook.add(donation_tab, text="Donation Logging")

        # Donation Input Fields
        tk.Label(donation_tab, text="Donor Name:").pack()
        self.donor_name_entry = tk.Entry(donation_tab)
        self.donor_name_entry.pack()

        tk.Label(donation_tab, text="Donated Items (comma-separated):").pack()
        self.donor_items_entry = tk.Entry(donation_tab)
        self.donor_items_entry.pack()

        tk.Button(donation_tab, text="Log Donation", command=self.log_donation).pack()

        # Donation List
        self.donation_listbox = tk.Listbox(donation_tab, height=10)
        self.donation_listbox.pack(fill=tk.BOTH, expand=True)
        tk.Button(donation_tab, text="Show Donations", command=self.show_donations).pack()

    def create_distribution_tab(self):
        distribution_tab = ttk.Frame(self.notebook)
        self.notebook.add(distribution_tab, text="Distribution Coordination")

        # Distribution Input Fields
        tk.Label(distribution_tab, text="Recipient Name:").pack()
        self.recipient_name_entry = tk.Entry(distribution_tab)
        self.recipient_name_entry.pack()

        tk.Label(distribution_tab, text="Distributed Items (comma-separated):").pack()
        self.recipient_items_entry = tk.Entry(distribution_tab)
        self.recipient_items_entry.pack()

        tk.Button(distribution_tab, text="Log Distribution", command=self.log_distribution).pack()

        # Distribution List
        self.distribution_listbox = tk.Listbox(distribution_tab, height=10)
        self.distribution_listbox.pack(fill=tk.BOTH, expand=True)
        tk.Button(distribution_tab, text="Show Distributions", command=self.show_distributions).pack()

    # Inventory Functions
    def add_inventory_item(self):
        try:
            name = self.inv_name_entry.get()
            type = self.inv_type_entry.get()
            quantity = int(self.inv_quantity_entry.get())
            expiration_date = date.fromisoformat(self.inv_expiration_entry.get())
            item_id = len(self.inventory_manager.food_items) + 1
            item = FoodItem(item_id, name, type, quantity, expiration_date)
            self.inventory_manager.add_food_item(item)
            messagebox.showinfo("Success", f"Added {name} to inventory.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_inventory(self):
        self.inventory_listbox.delete(0, tk.END)
        for item in self.inventory_manager.get_inventory():
            self.inventory_listbox.insert(tk.END, str(item))

    # Donation Functions
    def log_donation(self):
        donor_name = self.donor_name_entry.get()
        items = self.donor_items_entry.get().split(",")
        donation = Donation(donor_name, items)
        self.donation_logger.add_donation(donation)
        messagebox.showinfo("Success", f"Donation logged from {donor_name}.")

    def show_donations(self):
        self.donation_listbox.delete(0, tk.END)
        for donation in self.donation_logger.get_donations():
            self.donation_listbox.insert(tk.END, str(donation))

    # Distribution Functions
    def log_distribution(self):
        recipient_name = self.recipient_name_entry.get()
        items = self.recipient_items_entry.get().split(",")
        distribution = DistributionRecord(recipient_name, items)
        self.distribution_manager.add_distribution(distribution)
        messagebox.showinfo("Success", f"Distribution logged for {recipient_name}.")

    def show_distributions(self):
        self.distribution_listbox.delete(0, tk.END)
        for record in self.distribution_manager.get_distributions():
            self.distribution_listbox.insert(tk.END, str(record))


if __name__ == "__main__":
    app = FoodPantryApp()
    app.mainloop()
