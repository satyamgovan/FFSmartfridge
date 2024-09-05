from src.utilities.database_manager import DatabaseManager

def expiry_logger():
    db_manager = DatabaseManager('../../database/database.db')
    db_manager.remove_expired_items()
    db_manager.update_expiry_log()
