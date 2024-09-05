from src.utilities.database_manager import DatabaseManager

db_manager = DatabaseManager('../../database/database.db')


class InventoryController:
    def __init__(self, db_path):
        self.db = DatabaseManager(db_path)
        self.current_page = 1
        self.items_per_page = 8
        self.total_items = self.db.get_total_items_count()
        self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page

    def get_items_for_current_page(self):
        items = self.db.fetch_items_paginated('items', self.current_page, self.items_per_page)
        # Convert each tuple to a dictionary
        item_details_list = []
        for item in items:
            item_details = {
                "foodName": item[1],
                "description": item[2],
                "expiry_date": item[3],
                "quantity": item[4],
                "volume": item[5]
            }
            item_details_list.append(item_details)
        return item_details_list

    def get_all_item_details(self):
        # This will fetch all item details at once
        all_item_names = self.db.get_all_item_names()
        return [self.db.get_item_description(name) for name in all_item_names]

    def get_description(self, item_name):
        # Call the method from the DatabaseManager to get the item's description
        return self.db.get_item_description(item_name)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1


inventory_controller = InventoryController('../../database/database.db')
