from tkinter import messagebox
from src.utilities.database_manager import DatabaseManager
import logging


db_manager = DatabaseManager('../../database/database.db')
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class RemoveItem:
    def __init__(self):
        pass

    @staticmethod
    def calculate_total_volume():
        result = db_manager.select_all("items")
        total_volume = sum(item[4] * item[5] for item in result)
        return total_volume

    @staticmethod
    def remove_food(food_id, quantity_to_reduce):
        try:
            item_details = db_manager.conditional_select("items", "id", food_id)
            if not item_details:
                return "Item not found", None

            item = item_details[0]
            current_quantity = item[4]

            if quantity_to_reduce > current_quantity:
                return "Cannot remove more quantity than is available", None

            new_quantity = current_quantity - quantity_to_reduce

            if new_quantity > 0:
                db_manager.update("items", "quantity", new_quantity, "id", food_id)
            else:
                db_manager.delete("items", "id", food_id)

            new_total_volume = RemoveItem.calculate_total_volume()
            return None, new_total_volume

        except Exception as e:
            logging.error(f"Error removing food item {food_id}: {e}")
            return "An error occurred while removing the item", None

    @staticmethod
    def removeFoodGui(entry_1, entry_2):
        try:
            food_id = entry_1.get().strip()
            if not food_id:
                messagebox.showerror("Error", "Food ID cannot be empty")
                return False

            try:
                quantity_to_reduce = int(entry_2.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for quantity")
                return False

            error_message, new_total_volume = RemoveItem.remove_food(food_id, quantity_to_reduce)

            if error_message:
                messagebox.showerror("Error", error_message)
                return False

            messagebox.showinfo("Success", f"Item removed successfully. New total volume: {new_total_volume:.2f}")
            return True

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            logging.error(f"Unexpected error in removeFoodGui: {e}")
            return False

        finally:
            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')