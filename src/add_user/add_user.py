import sqlite3
import re
from src.utilities.database_manager import DatabaseManager
from tkinter import messagebox
import logging

# Configure logging
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

class UserManagement:
    def __init__(self, db_path):
        self.db_manager = DatabaseManager(db_path)
        self.selected_role = "User"  # Default role

    def set_role(self, role):
        self.selected_role = role

    def format_fullname(self, fullname):
        return ' '.join(word.capitalize() for word in fullname.split())

    def is_valid_username(self, username):
        return not self.db_manager.username_exists(username)

    def is_valid_email(self, email):
        return '@' in email and '.' in email

    def is_valid_contact(self, contact):
        return contact.isdigit() and len(contact) <= 11

    def is_valid_password(self, password):
        has_number = any(char.isdigit() for char in password)
        has_special = any(not char.isalnum() for char in password)
        return len(password) >= 6 and has_number and has_special

    def add_user(self, email, fullname, contact, username, password):
        # Format and validate inputs
        name = self.format_fullname(fullname)
        try:
            if not self.is_valid_username(username):
                raise ValueError("Username already exists.")
            if not self.is_valid_email(email):
                raise ValueError("Invalid email format.")
            if not self.is_valid_contact(contact):
                raise ValueError("Invalid contact number.")
            if not self.is_valid_password(password):
                raise ValueError("Invalid password format.")

            # Add user
            self.db_manager.insert_user(email, name, contact, username, password, self.selected_role)
            messagebox.showinfo("Success", "User added successfully.")
            return True

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
            logging.error(f"Validation Error: {ve}")
            return False
        except sqlite3.IntegrityError as ie:
            messagebox.showerror("Integrity Error", "A database integrity error occurred.")
            logging.error(f"Integrity Error: {ie}")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", "A database error occurred.")
            logging.error(f"Database Error: {e}")
            return False
        except Exception as e:
            messagebox.showerror("Error", "An unexpected error occurred.")
            logging.error(f"Unexpected Error: {e}")
            return False
        finally:
            logging.info("Attempted to add user.")

    @staticmethod
    def handle_add_user(entries, user_mgmt):
        email = entries['email'].get()
        name = entries['name'].get()
        contact = entries['contact'].get()
        username = entries['username'].get()
        password = entries['password'].get()

        user_mgmt.add_user(email, name, contact, username, password)

        for entry in entries.values():
            entry.delete(0, 'end')
