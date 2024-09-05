import sqlite3


# Hello Shreyas here, Check out txt file in FFSmartfridge\database\help.txt to find out how to use this class...
class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Create tables if not exists
        self.cursor.execute('''
                           CREATE TABLE IF NOT EXISTS items (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               foodName TEXT NOT NULL,
                               expiryDate DATE NOT NULL
                           )
                       ''')

        self.cursor.execute('''
                           CREATE TABLE IF NOT EXISTS expirylog (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               foodName TEXT NOT NULL,
                               expiryDate DATE NOT NULL,
                               UNIQUE(foodName, expiryDate)
                           )
                       ''')
        # Create trigger if not exists
        self.cursor.execute('''
                           CREATE TRIGGER IF NOT EXISTS remove_expired_entry
                           AFTER DELETE ON items
                           BEGIN
                               -- Check if the food entry is not present in items table
                               DELETE FROM expirylog
                               WHERE foodName = OLD.foodName
                                 AND expiryDate = OLD.expiryDate
                                 AND OLD.foodName IS NOT NULL
                                 AND OLD.expiryDate IS NOT NULL
                                 AND OLD.foodName NOT IN (SELECT foodName FROM items);
                           END;
                       ''')

    def remove_expired_items(self):
        # Remove expired items from items table
        self.cursor.execute('''
                           DELETE FROM expirylog
                           WHERE expiryDate < DATE('now')
                       ''')
        self.commit_changes()

    def update_expiry_log(self):
        # Insert entries into expirylog for items that will expire exactly 3 days from now
        self.cursor.execute('''
                           INSERT INTO expirylog (foodName, expiryDate, item_id)
                           SELECT DISTINCT foodName, expiryDate, id
                           FROM items
                           WHERE expiryDate = strftime('%d/%m/%Y','now', '+3 days')
                           AND (foodName, expiryDate) NOT IN (SELECT foodName, expiryDate FROM expirylog)
                       ''')
        self.commit_changes()


        return self.cursor.fetchall()

    def commit_changes(self):
        self.conn.commit()

    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert(self, table_name, values):
        placeholders = ', '.join(['?' for _ in values])
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def insert_user(self, email, name, contact, username, password, role):
        query = "INSERT INTO users (email, fullname, contact, username, password, role) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (email, name, contact, username, password, role))
        self.conn.commit()

    def insert_record(self, table_name, values):
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(insert_query, tuple(values.values()))
        self.conn.commit()

    def update(self, table_name, update_column, update_value, condition_column, condition_value):
        update_query = f"UPDATE {table_name} SET {update_column} = ? WHERE {condition_column} = ?"
        self.cursor.execute(update_query, (update_value, condition_value))
        self.conn.commit()

    def delete(self, table_name, condition_column, condition_value):
        delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?"
        self.cursor.execute(delete_query, (condition_value,))
        self.conn.commit()

    def select_all(self, table_name):
        select_all_query = f"SELECT * FROM {table_name}"
        self.cursor.execute(select_all_query)
        return self.cursor.fetchall()

    def conditional_select(self, table_name, condition_column, condition_value):
        select_query = f"SELECT * FROM {table_name} WHERE {condition_column} = ?"
        self.cursor.execute(select_query, (condition_value,))
        return self.cursor.fetchall()

    def conditional_select_multiple(self, table_name, conditions, condition_values):
        condition_columns = ' AND '.join([f"{column} = ?" for column in conditions])
        select_query = f"SELECT * FROM {table_name} WHERE {condition_columns}"
        self.cursor.execute(select_query, condition_values)
        return self.cursor.fetchall()

    def reduce_quantity(self, table_name, id_column, id_value, quantity_column, reduce_by):
        # Get current quantity
        self.cursor.execute(f"SELECT {quantity_column} FROM {table_name} WHERE {id_column} = ?", (id_value,))
        result = self.cursor.fetchone()
        if result:
            current_quantity = result[0]
            new_quantity = current_quantity - reduce_by

            if new_quantity <= 0:
                # Delete the row if quantity is 0 or less
                self.delete(table_name, id_column, id_value)
            else:
                # Update the quantity
                self.update(table_name, quantity_column, new_quantity, id_column, id_value)

    def select_low_quantity_items(self, table_name, quantity_column):
        select_query = f"SELECT *, (SELECT threshold FROM items WHERE items.id = {table_name}.id) AS threshold FROM {table_name} WHERE {quantity_column} < threshold"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def username_exists(self, username):
        query = "SELECT COUNT(*) FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def select_user_by_id(self, user_id):
        query = "Select * FROM users WHERE user_id =?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def fetch_head_chef_emails(self):
        # Execute the SQL statement to fetch email addresses of head chefs
        self.cursor.execute("SELECT email FROM users WHERE role = 'Head Chef';")
        head_chef_emails = self.cursor.fetchall()

        return head_chef_emails

    def fetch_food_items(self):
        # Fetch food items with their names and expiry dates
        self.cursor.execute("SELECT foodName, expiryDate FROM items;")
        food_items = self.cursor.fetchall()

        return food_items

    def fetch_supplier_info(self, supplier_id):
        try:
            query = "SELECT id, email, name FROM suppliers WHERE id = ?"

            cursor = self.conn.cursor()
            cursor.execute(query, (supplier_id,))
            supplier_info = cursor.fetchone()

            if supplier_info:
                return supplier_info
            else:
                return None
        except Exception as e:
            print(f"Error fetching supplier info: {e}")
            return None
        finally:
            cursor.close()

    def fetch_weekly_orders(self):
        try:
            query = "SELECT * FROM orders"
            self.cursor.execute(query)
            weekly_orders = self.cursor.fetchall()
            return weekly_orders
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def fetch_item_name(self, item_id):
        try:
            query = "SELECT foodName FROM items WHERE id = ?"

            cursor = self.conn.cursor()
            cursor.execute(query, (item_id,))
            item_name_result = cursor.fetchone()

            if item_name_result:
                item_name = item_name_result[0]
                return item_name
            else:
                return f"Item ID {item_id}"

        except Exception as e:
            print(f"Error fetching item name: {e}")
            return f"Item ID {item_id}"

        finally:
            cursor.close()

    # Delivery driver related functions

    def start_session(self, user_id, user_role):
        query = "INSERT INTO sessions (user_id, user_role, time_stamp) VALUES (?, ?, datetime('now'))"
        self.cursor.execute(query, (user_id, user_role))
        self.conn.commit()

    def get_current_session(self):
        """Retrieve the most recent active session without an end time."""
        select_query = "SELECT user_id, user_role FROM sessions WHERE end_time IS NULL ORDER BY time_stamp DESC LIMIT 1"
        self.cursor.execute(select_query)
        return self.cursor.fetchone()

    def end_session(self, user_id):
        """Update the current session's end time for the given user ID."""
        end_session_query = "UPDATE sessions SET end_time = datetime('now') WHERE user_id = ? AND end_time IS NULL"
        self.cursor.execute(end_session_query, (user_id,))
        self.conn.commit()

    def create_temp_items_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS temp_items (
                id INTEGER PRIMARY KEY,
                food_name TEXT,
                food_description TEXT,
                expiry_date DATE,
                quantity INTEGER,
                volume REAL
            )
        """)
        self.conn.commit()

    def insert_temp_item(self, unique_id, food_name, food_description, expiry_date, quantity, volume):
        self.cursor.execute("""
            INSERT INTO temp_items (id, food_name, food_description, expiry_date, quantity, volume)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (unique_id, food_name, food_description, expiry_date, quantity, volume))
        self.conn.commit()

    def get_temp_items(self):
        self.cursor.execute("SELECT * FROM temp_items")
        return self.cursor.fetchall()

    def clear_temp_items(self):
        self.cursor.execute("DELETE FROM temp_items")
        self.conn.commit()

    # Delivery driver related functions ends

    def get_total_items_count(self):
        query = "SELECT COUNT(*) FROM items"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def fetch_items_paginated(self, table_name, page, items_per_page):
        offset = (page - 1) * items_per_page
        paginated_query = f"SELECT * FROM {table_name} LIMIT ? OFFSET ?"
        self.cursor.execute(paginated_query, (items_per_page, offset))
        return self.cursor.fetchall()

    def search_items(self, search_term):
        actual_column_name = 'foodName'
        query = f"SELECT * FROM items WHERE {actual_column_name} LIKE ?"
        self.cursor.execute(query, ('%' + search_term + '%',))
        return self.cursor.fetchall()

    def get_all_item_names(self):
        self.cursor.execute("SELECT foodName FROM items")
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_item_description(self, item_name):
        query = """
                SELECT foodName, foodDescription, expiryDate, quantity, volume
                FROM items
                WHERE foodName = ?
                """
        self.cursor.execute(query, (item_name,))
        result = self.cursor.fetchone()
        if result:
            food_name, description, expiry_date, quantity, volume = result
            return {
                "foodName": food_name,
                "description": description,
                "expiry_date": expiry_date,
                "quantity": quantity,
                "volume": volume
            }
        else:
            return {
                "foodName": item_name,
                "description": "Description not found.",
                "expiry_date": "N/A",
                "quantity": "N/A",
                "volume": "N/A"
            }

    def fetch_user_access_logs(self, user_id):
        try:
            query = "SELECT user_role, time_stamp, end_time FROM sessions WHERE user_id = ? ORDER BY time_stamp DESC"
            self.cursor.execute(query, (user_id,))
            sessions = self.cursor.fetchall()

            # Print sessions for debugging
            print("User ID:", user_id)
            print("Sessions:", sessions)

            # Process sessions to create access logs
            access_logs = []
            for session in sessions:
                user_role, start_time, end_time = session
                access_logs.append(f"{user_role} session started at {start_time}")
                if end_time:
                    access_logs.append(f"{user_role} session ended at {end_time}")

            return access_logs
        except Exception as e:
            print(f"Error fetching user access logs: {e}")
            return []  # Return an empty list in case of an error

    def get_all_sessions(self):
        query = "SELECT * FROM sessions"
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def close_connection(self):
        self.conn.close()
