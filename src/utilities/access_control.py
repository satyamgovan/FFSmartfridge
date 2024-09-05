import logging
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


class AccessControl:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        try:
            # Initialize session data with error handling
            self.session_data = self.db_manager.get_current_session()
            self.user_role = self.session_data[1] if self.session_data else None
        except Exception as e:
            logging.error(f"Failed to initialize session data: {e}")
            self.session_data = None
            self.user_role = None

    def start_session(self, user_id, role):
        """Start a new session for the user."""
        try:
            self.user_role = role
            self.db_manager.start_session(user_id, role)
        except Exception as e:
            logging.error(f"Failed to start session for user {user_id}: {e}")

    def end_session(self):
        """End the current session for the logged-in user."""
        try:
            if self.session_data:
                user_id = self.session_data[0]
                self.db_manager.end_session(user_id)
                self.db_manager.clear_temp_items()  # Clear the temp_items table
                self.session_data = None
                self.user_role = None
        except Exception as e:
            logging.error(f"Failed to end session for user {user_id}: {e}")

    def has_access_to(self, gui_name):
        """Check if the user has access to the specified GUI based on their role."""
        allowed_guis = {
            'Delivery Driver': ['home', 'login', 'manual', 'delivery_display'],
            'Chef': ['home', 'login', 'manual', 'inventory', 'remove', 'delivery_display'],
            'Head Chef': ['home', 'inventory', 'login', 'manual', 'profile', 'remove', 'report', 'users', 'add_user', 'delivery_display'],
        }
        return gui_name in allowed_guis.get(self.user_role, [])
