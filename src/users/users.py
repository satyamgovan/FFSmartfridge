import sqlite3
from tkinter import PhotoImage, Button, messagebox
import logging
from src.utilities.database_manager import DatabaseManager
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def create_user_buttons(canvas, window_manager, photo_path_func, db_path, open_profile_callback, page=0, users_per_page=6):
    try:
        db_manager = DatabaseManager(db_path)
        users = db_manager.select_all('users')
        if not users:
            messagebox.showinfo("Info", "No users found.")
            return

        start_index = page * users_per_page
        end_index = start_index + users_per_page
        displayed_users = users[start_index:end_index]

        # Starting positions for the buttons
        x, y = 100.625, 100.7911376953125
        button_width, button_height = 296.2486267089844, 276.0029296875
        offset_x, offset_y = 400, 300

        for index, user in enumerate(displayed_users):
            pos_x = x + (index % 3) * offset_x
            pos_y = y + (index // 3) * offset_y

            user_id, name, role = user[0], user[2], user[6]

            button = Button(
                canvas,
                text=f"{name}\n({role})",
                compound='top',
                borderwidth=0,
                highlightthickness=0,
                command=lambda u_id=user_id: open_profile_callback(u_id),
                relief="flat",
            )
            button.place(x=pos_x, y=pos_y, width=button_width, height=button_height)

    except sqlite3.DatabaseError as e:
        messagebox.showerror("Database Error", "An error occurred while fetching users from the database.")
        logging.error(f"Database error in create_user_buttons: {e}")

