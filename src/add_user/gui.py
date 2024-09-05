from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from add_user import UserManagement
from src.utilities.window_manager import WindowManager
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/add_user")
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)

window = Tk()

window.geometry("1366x1024")
window.configure(bg = "#FFFFFF")
window_manager = WindowManager(window)

if not access_control.has_access_to('add_user'):
    messagebox.showerror("Access Denied", "You do not have permission to access the add users page.")
    window_manager.run_new_file('gui2')  # Redirect to login page
    exit()


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1024,
    width = 1366,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_1.place(
    x=133.9996566772461,
    y=912.0000344131698,
    width=92.87463894996318,
    height=64.58263737640175
)

canvas.create_text(
    1088.0,
    988.69873046875,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_2.place(
    x=1155.109375,
    y=916.0,
    width=78.36550903320312,
    height=61.951271057128906
)

canvas.create_text(
    154.0,
    988.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    59.99999997150633,
    25.0,
    anchor="nw",
    text="Add Users",
    fill="#000000",
    font=("CutiveMono Regular", 24 * -1)
)

canvas.create_text(
    71.99999998385363,
    192.0,
    anchor="nw",
    text="User Full Name:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    350.4999999824289,
    283.0000001322582,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=71.9999999648578,
    y=246.0,
    width=557.0000000351422,
    height=72.00000026451642
)

canvas.create_text(
    719.9999999838536,
    192.0,
    anchor="nw",
    text="Username:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    998.4999999824289,
    283.0000001322582,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=719.9999999648578,
    y=246.0,
    width=557.0000000351422,
    height=72.00000026451642
)

canvas.create_text(
    71.99999998385363,
    362.0,
    anchor="nw",
    text="Email:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    350.4999999824289,
    453.0000001322582,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=71.9999999648578,
    y=416.0,
    width=557.0000000351422,
    height=72.0000002645164
)

canvas.create_text(
    71.99999998385363,
    532.0,
    anchor="nw",
    text="Password:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    350.4999999824289,
    623.0000001322583,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=71.9999999648578,
    y=586.0,
    width=557.0000000351422,
    height=72.00000026451642
)

canvas.create_text(
    734.9999999838536,
    546.0,
    anchor="nw",
    text="Role:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    719.9999999838536,
    362.0,
    anchor="nw",
    text="Contact:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    998.4999999824289,
    453.0000001322582,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=719.9999999648578,
    y=416.0,
    width=557.0000000351422,
    height=72.0000002645164
)


user_mgmt = UserManagement('../../database/database.db')
def set_role_chef():
    try:
        user_mgmt.set_role("Chef")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred while setting role.")
        logging.error(f"set_role_chef Error: {e}")

def set_role_head_chef():
    try:
        user_mgmt.set_role("Head Chef")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred while setting role.")
        logging.error(f"set_role_head_chef Error: {e}")
def set_role_delivery_driver():
    try:
        user_mgmt.set_role("Delivery Driver")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred while setting role.")
        logging.error(f"set_role_delivery_driver Error: {e}")

# Dictionary to hold the Entry widgets for user information
entries = {
    'email': entry_3,
    'name': entry_1,
    'contact': entry_5,
    'username': entry_2,
    'password': entry_4
}


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: UserManagement.handle_add_user(entries, user_mgmt),
    relief="flat"
)
button_3.place(
    x=520.0,
    y=756.0,
    width=325.0,
    height=72.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=set_role_chef,
    relief="flat"
)
button_4.place(
    x=735.0,
    y=600.0,
    width=135.0,
    height=46.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=set_role_delivery_driver,
    relief="flat"
)
button_5.place(
    x=1134.0,
    y=600.0,
    width=135.0,
    height=46.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=set_role_head_chef,
    relief="flat"
)
button_6.place(
    x=910.0,
    y=600.0,
    width=188.0,
    height=46.0
)
window.resizable(False, False)
window.mainloop()
