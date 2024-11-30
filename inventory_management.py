import tkinter as tk
from tkinter import messagebox
from datetime import date


class FoodItem:
    """Represents a food item in the inventory."""
    def __init__(self, item_id, name, type, quantity, expiration_date):
        self.item_id = item_id
        self.name = name
        self.type = type
        self.quantity = quantity
        self.expiration_date = expiration_date

    def __str__(self):
        return f"{self.name} (Type: {self.type}, Quantity: {self.quantity}, Exp: {self.expiration_date})"


class InventoryManager:
    """Manages the inventory of food items."""
    def __init__(self):
        self.food_items = []

    def add_food_item(self, item):
        """Adds a food item to the inventory."""
        self.food_items.append(item)

    def update_stock(self, item_id, new_quantity):
        """Updates the quantity of a food item."""
        for item in self.food_items:
            if item.item_id == item_id:
                item.quantity = new_quantity
                return True
        return False

    def monitor_expiration(self):
        """Lists food items nearing expiration."""
        today = date.today()
        expiring_items = [
            item for item in self.food_items
            if (item.expiration_date - today).days <= 7
        ]
        return expiring_items

    def get_inventory(self):
        """Returns a list of all food items."""
        return self.food_items


# Week 1 GUI
class InventoryGUI(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.title("Inventory Management")
        self.geometry("500x400")

        tk.Label(self, text="Food Item Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Type (e.g., Non-perishable):").pack()
        self.type_entry = tk.Entry(self)
        self.type_entry.pack()

        tk.Label(self, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack()

        tk.Label(self, text="Expiration Date (YYYY-MM-DD):").pack()
        self.expiration_entry = tk.Entry(self)
        self.expiration_entry.pack()

        tk.Button(self, text="Add Food Item", command=self.add_item).pack()

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        tk.Button(self, text="Show Inventory", command=self.show_inventory).pack()

    def add_item(self):
        try:
            name = self.name_entry.get()
            type = self.type_entry.get()
            quantity = int(self.quantity_entry.get())
            expiration_date = date.fromisoformat(self.expiration_entry.get())
            item_id = len(self.manager.food_items) + 1
            item = FoodItem(item_id, name, type, quantity, expiration_date)
            self.manager.add_food_item(item)
            messagebox.showinfo("Success", f"Added {name} to inventory.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_inventory(self):
        self.listbox.delete(0, tk.END)
        for item in self.manager.get_inventory():
            self.listbox.insert(tk.END, str(item))


if __name__ == "__main__":
    inventory_manager = InventoryManager()
    app = InventoryGUI(inventory_manager)
    app.mainloop()