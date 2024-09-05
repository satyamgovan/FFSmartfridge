from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Entry, StringVar, TclError, messagebox
import logging
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from users import create_user_buttons
from src.utilities.window_manager import WindowManager


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Define the path to your assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("../../img/users")
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Initialize the main window
window = Tk()
window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

# Instantiate your WindowManager
window_manager = WindowManager(window)

if not access_control.has_access_to('users'):
    messagebox.showerror("Access Denied", "You do not have permission to access the users page.")
    window_manager.run_new_file('gui2')
    exit()

global current_page
current_page = 0
USERS_PER_PAGE = 6

def refresh_display():
    global current_page
    try:
        for widget in canvas.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()
        create_user_buttons(canvas, window_manager, relative_to_assets, '../../database/database.db', open_user_profile, current_page)
    except Exception as e:
        messagebox.showerror("Refresh Error", "An error occurred while refreshing the display.")
        logging.error(f"Error refreshing display: {e}")

def go_to_next_page():
    global current_page
    try:
        current_page += 1
        refresh_display()
    except Exception as e:
        messagebox.showerror("Navigation Error", "An error occurred while navigating to the next page.")
        logging.error(f"Error going to next page: {e}")

def go_to_previous_page():
    global current_page
    try:
        if current_page > 0:
            current_page -= 1
            refresh_display()
        else:
            messagebox.showinfo("Navigation Info", "Already at the first page.")
    except Exception as e:
        messagebox.showerror("Navigation Error", "An error occurred while navigating to the previous page.")
        logging.error(f"Error going to previous page: {e}")


# Create a canvas where the buttons will be placed
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=1024,
    width=1366,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

def open_user_profile(user_id):
    window_manager.run_new_file('gui6', user_id)

button_width = 100
button_height = 30

# Gap between buttons and from the bottom edge of the window
gap_from_bottom = 200
gap_between_buttons = 50

window_width = 1366
window_height = 1024

prev_button_x = (window_width - 2 * button_width - gap_between_buttons) / 2
prev_button_y = window_height - button_height - gap_from_bottom


prev_page_button = Button(window, text="Previous", command=go_to_previous_page)
prev_page_button.place(x=prev_button_x, y=prev_button_y, width=button_width, height=button_height)

next_button_x = prev_button_x + button_width + gap_between_buttons
next_button_y = prev_button_y

next_page_button = Button(window, text="Next", command=go_to_next_page)
next_page_button.place(x=next_button_x, y=next_button_y, width=button_width, height=button_height)

create_user_buttons(canvas, window_manager, relative_to_assets, '../../database/database.db', open_user_profile,
                    current_page, USERS_PER_PAGE)

refresh_display()

canvas.create_text(
    45.99999994728671,
    16.0,
    anchor="nw",
    text="Manage Users",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_7.place(
    x=160.9996566772461,
    y=890.0000344131698,
    width=92.87463894996318,
    height=64.58263737640175
)

canvas.create_text(
    1085.0,
    968.6986083984375,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_8.place(
    x=1152.109375,
    y=896.0,
    width=78.36550903320312,
    height=61.951271057128906
)

canvas.create_text(
    181.0,
    966.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    620.0,
    966.0,
    anchor="nw",
    text="Add User",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
user_id_for_button_9 = 'some_user_id'
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui10', user_id_for_button_9),
    relief="flat"
)
button_9.place(
    x=648.0,
    y=883.0,
    width=69.0927734375,
    height=69.0927734375
)
window.resizable(False, False)
window.mainloop()