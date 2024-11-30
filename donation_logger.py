from datetime import date

class Donation:
    """Represents a donation."""
    def __init__(self, donor_name, items):
        self.donor_name = donor_name
        self.items = items  # List of FoodItem objects
        self.date = date.today()

    def __str__(self):
        return f"Donation by {self.donor_name} on {self.date}"


class DonationLogger:
    """Logs and manages donations."""
    def __init__(self):
        self.donations = []

    def add_donation(self, donation):
        """Logs a new donation."""
        self.donations.append(donation)

    def get_donations(self):
        """Returns a list of all donations."""
        return self.donations