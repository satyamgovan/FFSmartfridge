import random
from src.utilities.database_manager import DatabaseManager
from datetime import datetime
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
import logging


db_manager = DatabaseManager('../../database/database.db')
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class ManualEntry:
    def __init__(self):
        self.supplier_mapping = {
            'Egg': {'supplier_id': 1, 'threshold': 15},
            'Butter': {'supplier_id': 2, 'threshold': 10},
            'Milk': {'supplier_id': 1, 'threshold': 12},
            'Onion': {'supplier_id': 2, 'threshold': 15},
            'Tomato': {'supplier_id': 3, 'threshold': 10},
            'Parsley': {'supplier_id': 2, 'threshold': 20},
            'Fish': {'supplier_id': 1, 'threshold': 8},
            'Cheese': {'supplier_id': 3, 'threshold': 5},
            'Chicken': {'supplier_id': 1, 'threshold': 10},
            'Lemon': {'supplier_id': 2, 'threshold': 12},
        }

    @staticmethod
    def generate_id():
        return random.randint(10000, 99999)

    @staticmethod
    def exists(unique_id):
        result = db_manager.conditional_select("items", "id", unique_id)
        return bool(result)

    @staticmethod
    def calculate_volume():
        result = db_manager.select_all("items")
        total_volume = sum(item[4] * item[5] for item in result)
        return total_volume

    @staticmethod
    def get_current_user_role():
        current_session = db_manager.get_current_session()
        if current_session:
            user_role = current_session[1]
            return user_role
        return None

    def check_order(self, food_name, quantity):
        scanned_food_name = food_name.lower()
        orders = db_manager.select_all("orders")

        matching_order = None
        for order in orders:
            order_food_name = order[6].lower()
            order_quantity = order[5]

            if order_food_name == scanned_food_name:
                if order_quantity == quantity:
                    matching_order = order
                    break
                else:
                    messagebox.showerror(
                        "Order Quantity Mismatch",
                        f"The item {food_name} does not match the required quantity.\n"
                        f"Required quantity: {order_quantity}"
                    )
                    return None

        if matching_order:
            return matching_order

        if not any(order[6].lower() == scanned_food_name for order in orders):
            messagebox.showerror("Order Not Found", f"No order found for the item {food_name}.")

        return None

    def submit_entry(self, food_name, food_description, expiry_date, quantity, volume):
        try:
            total_volume = self.calculate_volume()

            # Fridge capacity check
            if total_volume + (quantity * volume) > 440:
                messagebox.showinfo("Full", "Not enough space in the fridge")
                return False

            existing_item = db_manager.conditional_select_multiple("items", ["foodName", "expiryDate"],
                                                                   (food_name, expiry_date))

            if existing_item:
                existing_quantity = existing_item[0][4]
                new_quantity = existing_quantity + quantity
                db_manager.update("items", "quantity", new_quantity, "foodName", food_name)
            else:
                unique_id = self.generate_id()
                while self.exists(unique_id):
                    unique_id = self.generate_id()

                supplier_info = self.supplier_mapping.get(food_name, {'supplier_id': 0, 'threshold': 0})
                supplier_id = supplier_info['supplier_id']
                threshold = supplier_info['threshold']

                db_manager.create_table("items",
                                        "id INTEGER PRIMARY KEY, foodName TEXT, foodDescription TEXT, expiryDate DATE, quantity INTEGER, volume REAL, supplier_id INTEGER, threshold INTEGER")
                item_values = (
                    unique_id, food_name, food_description, expiry_date, quantity, volume, supplier_id, threshold)

                user_role = self.get_current_user_role()
                if user_role == "Delivery Driver":
                    order = self.check_order(food_name, quantity)
                    if order:
                        db_manager.insert("items", item_values)
                        db_manager.insert_temp_item(unique_id, food_name, food_description, expiry_date, quantity, volume)
                        db_manager.delete("orders", "id", order[0])
                        messagebox.showinfo("Order Matched", f"Order matched and removed: {order}")
                        return True
                    else:
                        messagebox.showerror("Order Mismatch", "The entered item does not match any orders.")
                        return False
                else:
                    db_manager.insert("items", item_values)
                    db_manager.insert_temp_item(unique_id, food_name, food_description, expiry_date, quantity, volume) #Adds items to temp table to display

            return True
        except Exception as e:
            logging.error(f"Error in submit_entry: {e}")
            messagebox.showerror("Database Error", f"An error occurred while submitting the entry: {e}")
            return False

    # Increase quantity
    @staticmethod
    def increase_quantity(entry_4):
        current_value = int(entry_4.get())
        entry_4.delete(0, 'end')
        entry_4.insert(0, str(current_value + 1))

    # Decrease quantity
    @staticmethod
    def decrease_quantity(entry_4):
        current_value = int(entry_4.get())
        if current_value > 0:
            entry_4.delete(0, 'end')
            entry_4.insert(0, str(current_value - 1))

    # Validator for expiry date
    @staticmethod
    def date_validation(expiry_date):
        date_format = '%d/%m/%Y'
        return datetime.strptime(expiry_date, date_format) if expiry_date.count('/') == 2 else False

    # Takes the information from the GUI
    def submit_entry_gui(self, entry_1, entry_2, entry_3, entry_4, entry_5):
        try:
            food_name = entry_1.get()
            food_description = entry_2.get("1.0", "end-1c")
            expiry_date = entry_3.get()
            quantity = int(entry_4.get())
            volume = float(entry_5.get())

            # Check if any entry is null
            if not all([food_name, expiry_date]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Display a pop-up messagebox when an invalid date format is entered
            if not self.date_validation(expiry_date):
                messagebox.showerror("Incorrect date format",
                                     "Invalid format. Please enter a date in the format DD/MM/YYYY.")
                return

            user_role = ManualEntry.get_current_user_role()
            entry_success = self.submit_entry(food_name, food_description, expiry_date, quantity, volume)

            if entry_success:
                entry_1.delete(0, 'end')
                entry_2.delete('1.0', 'end')
                entry_3.delete(0, 'end')
                entry_4.delete(0, 'end')
                entry_5.delete(0, 'end')
        except ValueError as e:
            logging.error(f"ValueError in submit_entry_gui: {e}")
            messagebox.showerror("Input Error", "Please enter valid numbers for quantity and volume.")
        except Exception as e:
            logging.error(f"Unhandled error in submit_entry_gui: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Read QR code from camera and print information
    @staticmethod
    def read_qr(entry_1, entry_2, entry_3, entry_5):
        try:
            cap = cv2.VideoCapture(0)  # Open default camera

            while True:
                ret, frame = cap.read()
                decoded_objects = decode(frame)

                for obj in decoded_objects:
                    qr_data = obj.data.decode('utf-8')

                    qr_lines = qr_data.split("\n")

                    # Check if the QR code follows the expected format
                    if len(qr_lines) >= 4 and qr_lines[0].startswith("Item Name:") \
                            and qr_lines[1].startswith("Description:") and qr_lines[2].startswith("Expiry Date:") \
                            and qr_lines[3].startswith("Volume:"):
                        # Fill the entries with information from the scanned QR code
                        entry_1.delete(0, 'end')
                        entry_1.insert(0, qr_lines[0].split(":")[1].strip())

                        entry_2.delete('1.0', 'end')
                        entry_2.insert('1.0', qr_lines[1].split(":")[1].strip())

                        entry_3.delete(0, 'end')
                        entry_3.insert(0, qr_lines[2].split(":")[1].strip())

                        entry_5.delete(0, 'end')
                        entry_5.insert(0, qr_lines[3].split(":")[1].strip())

                        # Close the camera window after reading the QR code
                        cap.release()
                        cv2.destroyAllWindows()

                        return

                cv2.imshow("QR Code Scanner", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except Exception as e:
            logging.error(f"Error in read_qr_code_from_camera: {e}")
            messagebox.showerror("QR Code Error", f"An error occurred during QR code scanning: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()