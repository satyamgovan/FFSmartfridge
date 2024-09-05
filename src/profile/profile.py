import logging
from src.utilities.database_manager import DatabaseManager
db_manager = DatabaseManager('../../database/database.db')
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class Profile:
    def __init__(self, db_path):
        self.db_manager = DatabaseManager(db_path)

    def get_user_profile(self, user_id):
        try:
            user_data = self.db_manager.select_user_by_id(user_id)
            return user_data
        except Exception as e:
            logging.error(f"Error in get_user_profile: {e}")
            raise

    def update_user_profile(self, user_id, email, name, contact, role):
        try:
            self.db_manager.update('users', 'email', email, 'user_id', user_id)
            self.db_manager.update('users', 'fullname', name, 'user_id', user_id)
            self.db_manager.update('users', 'contact', contact, 'user_id', user_id)
            self.db_manager.update('users', 'role', role, 'user_id', user_id)
        except Exception as e:
            logging.error(f"Error in update_user_profile: {e}")
            raise

    def delete_user_profile(self, user_id):
        try:
            self.db_manager.delete('users', 'user_id', user_id)
        except Exception as e:
            logging.error(f"Error in delete_user_profile: {e}")
            raise
