import sys
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox,Entry
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from src.utilities.window_manager import WindowManager
import logging

db_manager = DatabaseManager('../../database/database.db')

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/profile")

access_control = AccessControl(db_manager)
db_manager = DatabaseManager('../../database/database.db')
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1366x1024")
window.configure(bg = "#FFFFFF")
window_manager = WindowManager(window)

if not access_control.has_access_to('profile'):
    messagebox.showerror("Access Denied", "You do not have permission to access the profile page.")
    window_manager.run_new_file('gui2')
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

canvas.create_text(
    24.999999964857807,
    3.0,
    anchor="nw",
    text="Manage Users",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    682.0,
    188.0,
    image=image_image_1
)

name_text_id = canvas.create_text(
    526.0,
    336.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

userid_text_id = canvas.create_text(
    524.0,
    386.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)


canvas.create_rectangle(
    303.0,
    458.0,
    1113.0,
    564.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    303.0,
    586.0,
    1113.0,
    692.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    303.0,
    714.0,
    1113.0,
    820.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    335.0,
    491.0,
    anchor="nw",
    text="Email:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)



canvas.create_text(
    335.0,
    621.0,
    anchor="nw",
    text="Contact:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)



image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    797.0,
    403.0,
    image=image_image_2
)


contact_text_id = canvas.create_text(
    568.0,
    619.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_rectangle(
    525.0,
    457.0,
    526.0,
    564.0,
    fill="#666666",
    outline="")



canvas.create_rectangle(
    525.0,
    585.0,
    526.0,
    692.0,
    fill="#666666",
    outline="")

canvas.create_rectangle(
    525.0,
    713.0,
    526.0,
    820.0,
    fill="#666666",
    outline="")

email_text_id = canvas.create_text(
    568.0,
    491.0,
    anchor="nw",
    text="",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)


selected_user_id = sys.argv[1] if len(sys.argv) > 1 else '1'
def display_user_data(user_id):
    try:
        user_data = db_manager.select_user_by_id(user_id)
        if user_data:
            canvas.itemconfigure(name_text_id, text=user_data[1])  # Name
            canvas.itemconfigure(userid_text_id, text=user_data[0])  # UserID
            canvas.itemconfigure(contact_text_id, text=user_data[4])  # Contact
            canvas.itemconfigure(email_text_id, text=user_data[3])  # Email
        else:
            messagebox.showinfo("User Not Found", f"No user found with ID: {user_id}")
    except Exception as e:
        messagebox.showerror("Database Error", "An error occurred while fetching user data.")
        logging.error(f"Database error when fetching user data for ID {user_id}: {e}")


display_user_data(selected_user_id)
# Function to update user role
def update_user_role(user_id, new_role):
    try:
        db_manager.update('users', 'role', new_role, 'user_id', user_id)
        messagebox.showinfo("Success", f"User {user_id}'s role updated to {new_role}.")
        display_user_data(user_id)  # Refresh the displayed data
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while updating the user role.")
        logging.error(f"Error updating user role for ID {user_id}: {e}")


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_user_role(selected_user_id, "Chef"),
    relief="flat"
)
button_1.place(
    x=552.0,
    y=744.0,
    width=135.0,
    height=46.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_user_role(selected_user_id, "Delivery Driver"),
    relief="flat"
)
button_2.place(
    x=951.0,
    y=744.0,
    width=135.0,
    height=46.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_user_role(selected_user_id, "Head Chef"),
    relief="flat"
)
button_3.place(
    x=727.0,
    y=744.0,
    width=188.0,
    height=46.0
)

canvas.create_text(
    368.0,
    745.0,
    anchor="nw",
    text="Role:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_4.place(
    x=172.9996566772461,
    y=896.0000344131698,
    width=92.87463894996318,
    height=64.58263737640175
)

canvas.create_text(
    1097.0,
    974.6986083984375,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_5.place(
    x=1164.109375,
    y=902.0,
    width=78.36550903320312,
    height=61.951271057128906
)

canvas.create_text(
    193.0,
    972.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    615.0,
    959.999755859375,
    anchor="nw",
    text="Remove User",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

def delete_user():
    user_id = selected_user_id
    try:
        if messagebox.askyesno("Delete User", "Are you sure you want to delete this user?"):
            db_manager.delete('users', 'user_id', user_id)
            messagebox.showinfo("Success", f"User with ID {user_id} deleted successfully.")
            selected_user_id.delete(0, 'end')
    except Exception as e:
        window_manager.run_new_file('gui9')


button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=delete_user,
    relief="flat"
)
button_6.place(
    x=647.0,
    y=925.0,
    width=84.0,
    height=21.0
)

window.resizable(False, False)
window.mainloop()
db_manager.close_connection()