import datetime
import time


class OrderScheduler:
    def __init__(self, database_manager, email_sender):
        self.database_manager = database_manager
        self.email_sender = email_sender

    def update_orders(self):
        try:
            # Fetch items with low quantity
            low_stock_items = self.database_manager.select_low_quantity_items('items', 'quantity')

            for item in low_stock_items:
                item_id, quantity, threshold, supplier_id = item[0], item[4], item[7], item[6]

                existing_order = self.database_manager.conditional_select('orders', 'item_id', item_id)

                remaining_quantity = max(threshold - quantity, 0)

                if existing_order and remaining_quantity > 0:
                    new_accumulated_quantity = remaining_quantity
                    self.database_manager.update(
                        'orders', 'accumulated_quantity', new_accumulated_quantity, 'item_id', item_id
                    )
                elif remaining_quantity > 0:
                    item_name = self.database_manager.fetch_item_name(item_id)
                    self.place_order(item_id, supplier_id, remaining_quantity, item_name)

            print("Committing changes...")
            self.database_manager.commit_changes()

        except Exception as e:
            print(f"Error during update_orders: {e}")

    def place_order(self, item_id, supplier_id, accumulated_quantity, item_name):
        # Insert a new order
        order_data = {
            'item_id': item_id,
            'supplier_id': supplier_id,
            'order_details': f"Order for {item_name}",
            'order_date': time.time(),
            'accumulated_quantity': accumulated_quantity,
            'item_name': item_name
        }

        self.database_manager.insert_record('orders', order_data)

    def send_order_emails(self, sender_email, sender_password):
        try:
            if datetime.datetime.now().weekday() == 0:  # Monday is 0
                weekly_orders = self.database_manager.fetch_weekly_orders()

                orders_by_supplier = {}
                for order in weekly_orders:
                    supplier_id = order[2]
                    if supplier_id not in orders_by_supplier:
                        orders_by_supplier[supplier_id] = []
                    orders_by_supplier[supplier_id].append(order)

                # Send emails to suppliers
                for supplier_id, supplier_orders in orders_by_supplier.items():
                    supplier_info = self.database_manager.fetch_supplier_info(supplier_id)
                    supplier_email = supplier_info[1] if supplier_info else None
                    supplier_name = supplier_info[2] if supplier_info else None

                    if supplier_email and supplier_name:
                        subject = f"Order Request for {supplier_name}"

                        body = f"Dear {supplier_name},\n\nBelow is the list of items we would like to order from your company:\n\n"

                        for order in supplier_orders:
                            order_id = order[0]
                            item_id = order[1]
                            quantity = order[5]

                            # Fetch item name from the items table
                            item_name_query = "SELECT foodName FROM items WHERE id = ?"
                            self.database_manager.cursor.execute(item_name_query, (item_id,))
                            item_name_result = self.database_manager.cursor.fetchone()
                            item_name = item_name_result[0] if item_name_result else f"Item ID {item_id}"

                            body += f"Order ID: {order_id}, Item ID: {item_id}, Item Name: {item_name}, Quantity: {quantity}\n"

                        body += "\nThank you for your attention to this matter.\n\nBest regards,\nFFSmartfridge"

                        self.email_sender.sender_email = sender_email
                        self.email_sender.sender_password = sender_password

                        self.email_sender.send_custom_email(supplier_email, subject, body)

                    print("Order emails sent on Monday.")
            else:
                print("Order emails are only sent on Mondays.")

        except Exception as e:
            print(f"Error during send_order_emails: {e}")

