import logging
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

class DeliveryDisplay:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_delivery_items(self):
        try:
            # Fetch data from the database
            rows = self.db_manager.get_temp_items()
            # Convert each row to a dictionary
            items = [
                {'food_name': row[1], 'food_description': row[2], 'expiry_date': row[3],
                 'quantity': row[4], 'volume': row[5]}
                for row in rows
            ]
            return items
        except Exception as e:
            logging.error(f"Error fetching delivery items: {e}. List cannot be displayed.")
            return []

    def clear_delivery_items(self):
        try:
            self.db_manager.clear_temp_items()
        except Exception as e:
            logging.error(f"Error clearing delivery items: {e}")
            raise