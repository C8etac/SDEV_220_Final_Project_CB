from database import connect_db

class Donations:
    @staticmethod
    def log_donation(name, type_, quantity, donation_date):
        """
        Logs a donation to the database.

        Args:
            name (str): Name of the donated item.
            type_ (str): Type of the item donated.
            quantity (int): Quantity of the item donated.
            donation_date (str): Date of the donation in YYYY-MM-DD format.
        """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (name, type, quantity, donation_date)
            VALUES (?, ?, ?, ?)
        """, (name, type_, quantity, donation_date))
        conn.commit()
        conn.close()

    @staticmethod
    def get_donations():
        """
        Retrieves all donation records from the database.

        Returns:
            list: A list of tuples, each containing a donation record.
        """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, donation_date FROM donations")
        donations = cursor.fetchall()
        conn.close()
        return donations