from pathlib import Path
from tkinter import Tk, Text, Button, Canvas, WORD, PhotoImage
from tkinter import messagebox
import logging
from src.utilities.window_manager import WindowManager
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from delivery_display import DeliveryDisplay

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/delivery_display")
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)
delivery_display = DeliveryDisplay(db_manager)
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)

if not access_control.has_access_to('delivery_display'):
    messagebox.showerror("Access Denied", "You do not have permission to access the delivery display page.")
    window_manager.run_new_file('gui2')
    exit()

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

# Function to display delivery items
def display_delivery_items():
    try:
        delivery_items = delivery_display.get_delivery_items()

        text_widget.delete(1.0, "end")
        for i, item in enumerate(delivery_items):
            # Add each item to the Text widget
            text_widget.insert("end", f"Item {i+1}:\nFood Name: {item['food_name']}\nDescription: {item['food_description']}\nExpiry Date: {item['expiry_date']}\nQuantity: {item['quantity']}\nVolume: {item['volume']}\n\n")
    except Exception as e:
        logging.error(f"Error displaying delivery items: {e}")
        messagebox.showerror("Error", "An error occurred while fetching delivery items.")


text_widget = Text(
    window,
    bg="#FFFFFF",
    font=("CutiveMono Regular", 26 * -1),
    fg="black",
    wrap=WORD,
)
text_widget.pack()

# Create a button to trigger the display_delivery_items function
display_button = Button(
    text="Display Added items",
    command=display_delivery_items,
)
display_button.pack()

#LOG OUT BUTTON
button_image_1 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_1.place(
    x=1212.1103515625,
    y=887.0,
    width=78.365478515625,
    height=61.951263427734375
)

canvas.create_text(
    1185.0,
    958.721435546875,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)
# Back Button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_2.place(
    x=86.9996337890625,
    y=886.0000305175781,
    width=92.87466430664062,
    height=64.5826416015625
)
canvas.create_text(
    106.9993896484375,
    960.9999389648438,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

# Call Assistance Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_3.place(
    x=645.0,
    y=881.0,
    width=75.93650817871094,
    height=73.96893310546875
)

canvas.create_text(
    564.0,
    959.0,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

window.resizable(False, False)
window.mainloop()