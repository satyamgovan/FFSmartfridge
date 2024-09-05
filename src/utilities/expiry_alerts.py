from datetime import datetime, timedelta
from src.utilities.database_manager import DatabaseManager
from src.utilities.notification_manager import EmailSender
from tkinter import messagebox

database_manager = DatabaseManager('../../database/database.db')

def send_expiry_notification(expiring_items):
    message = ""
    for food_name, days_until_expiry in expiring_items:
        message += f"{food_name} will expire in {days_until_expiry} days.\n"
    messagebox.showinfo("Expiry Reminder", message)

def check_expiry_alerts():
    today = datetime.now()
    food_items = database_manager.fetch_food_items()

    expiring_items = []

    for food_item in food_items:
        food_name, expiry_date_str = food_item
        expiry_date = datetime.strptime(expiry_date_str, "%d/%m/%Y")
        days_until_expiry = (expiry_date - today).days

        # Collect information about expiring items
        if 0 < days_until_expiry <= 3:
            expiring_items.append((food_name, days_until_expiry))

    # Trigger notification with all expiring items
    if expiring_items:
        send_expiry_notification(expiring_items)

        email_sender = EmailSender()
        email_sender.send_expiry_notification_email(expiring_items)

# check_expiry_alerts()