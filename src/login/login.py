from src.utilities.database_manager import DatabaseManager
from src.utilities.OrderScheduler import OrderScheduler
from src.utilities.notification_manager import EmailSender
from tkinter import messagebox
import datetime
import logging


logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

class LoginSystem:
    def __init__(self, db_path):
        self.db_manager = DatabaseManager(db_path)
        self.email_sender = EmailSender()

    def validate_login(self, username, password):
        try:
            user_result = self.db_manager.conditional_select("users", "username", username)
            if user_result:
                user_id, stored_password, user_role = user_result[0][0], user_result[0][5], user_result[0][6]
                if stored_password == password:
                    return user_id, user_role
            return None, None
        except Exception as e:
            logging.error(f"Login validation error: {e}")
            messagebox.showerror("Error", "An error occurred while validating login.")
            return None, None

    def handle_login(self, entry_1, entry_2, window_manager):
        try:
            username = entry_1.get()
            password = entry_2.get()

            user_id, user_role = self.validate_login(username, password)
            if user_id and user_role:
                self.db_manager.start_session(user_id, user_role)  # Start session in the database
                messagebox.showinfo("Login Success", "You have successfully logged in.")

                order_manager = OrderScheduler(self.db_manager, self.email_sender)
                order_manager.update_orders()

                window_manager.run_new_file('gui2')

                # Move the condition to send order emails inside the if block
                if datetime.datetime.now().weekday() == 0:  # Monday is 0
                    order_manager.send_order_emails(sender_email=self.email_sender.sender_email,
                                                    sender_password=self.email_sender.sender_password)
                    messagebox.showinfo("Monday", "Order emails are send successfully!")
                else:
                    print("Not Monday", "Order emails are only sent on Mondays.")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Exception as e:
            logging.error(f"Login handling error: {e}")
            messagebox.showerror("Error", "An unexpected error occurred during login.")
