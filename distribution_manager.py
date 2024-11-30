from datetime import date

class DistributionRecord:
    """Represents a distribution record."""
    def __init__(self, recipient_name, items):
        self.recipient_name = recipient_name
        self.items = items  # List of FoodItem objects
        self.date = date.today()

    def __str__(self):
        return f"Distribution to {self.recipient_name} on {self.date}"


class DistributionManager:
    """Manages food distribution records."""
    def __init__(self):
        self.distributions = []

    def add_distribution(self, record):
        """Logs a new distribution record."""
        self.distributions.append(record)

    def get_distributions(self):
        """Returns a list of all distributions."""
        return self.distributions