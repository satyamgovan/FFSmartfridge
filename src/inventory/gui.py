import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from src.utilities.access_control import AccessControl
from src.utilities.window_manager import WindowManager
from src.utilities.notification_manager import EmailSender
from src.utilities.expiry_alerts import check_expiry_alerts
from src.utilities.database_manager import DatabaseManager
from src.inventory.inventory import InventoryController
from src.utilities.expiry_log import expiry_logger

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/inventory")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)

inventory_controller = InventoryController('../../database/database.db')
expiry_logger()

def search_items(event=None):
    search_term = entry_1.get().strip()
    if search_term:
        # Search and fetch details for the items that match the search term
        search_results = db_manager.search_items(search_term)

        # Clear existing item labels and frames
        for frame_ref, text_ref in item_text_references:
            canvas.delete(frame_ref)
            canvas.delete(text_ref)
        item_text_references.clear()

        # Create labels for each search result
        for index, item_detail in enumerate(search_results):
            if index >= 8:  # Limit the search results to 8 items
                break
            position = item_positions[index]

            # Create a frame around each item's details
            frame_width = 200
            frame_height = 150
            frame = canvas.create_rectangle(
                position[0] - frame_width / 2, position[1] - frame_height / 2,
                position[0] + frame_width / 2, position[1] + frame_height / 2,
                outline="#000000", width=2
            )

            display_text = (f"Name: {item_detail[1]}\n"
                            f"Desc: {item_detail[2][:30]}...\n"
                            f"Exp: {item_detail[3]}\n"
                            f"Qty: {item_detail[4]}\n"
                            f"Vol: {item_detail[5]}")

            text_ref = canvas.create_text(
                position[0], position[1],
                anchor="center",
                text=display_text,
                fill="#000000",
                font=("CutiveMono Regular", 14 * -1),
                width=frame_width - 10
            )
            item_text_references.append((frame, text_ref))
    else:
        # If the search term is empty, display the default set of items
        update_items_display()


def update_items_display():
    # Fetch new page details
    all_item_details = inventory_controller.get_items_for_current_page()

    # Clear existing item labels and frames
    for frame_ref, text_ref in item_text_references:
        canvas.delete(frame_ref)
        canvas.delete(text_ref)
    item_text_references.clear()

    # Create and display new labels with updated item details and frames
    for index, item_detail in enumerate(all_item_details):
        if index >= len(item_positions):
            break

        # Check if item_detail is a dictionary and has the key 'foodName', else skip
        if isinstance(item_detail, dict) and 'foodName' in item_detail:
            position = item_positions[index]

            # Create a frame around each item's details
            frame_width = 200
            frame_height = 150
            frame = canvas.create_rectangle(
                position[0] - frame_width / 2, position[1] - frame_height / 2,
                position[0] + frame_width / 2, position[1] + frame_height / 2,
                outline="#000000", width=2
            )

            display_text = (f"Name: {item_detail['foodName']}\n"
                            f"Desc: {item_detail['description'][:30]}\n"
                            f"Exp: {item_detail['expiry_date']}\n"
                            f"Qty: {item_detail['quantity']}\n"
                            f"Vol: {item_detail['volume']}")

            text_ref = canvas.create_text(
                position[0], position[1],
                anchor="center",
                text=display_text,
                fill="#000000",
                font=("CutiveMono Regular", 14 * -1),
                width=frame_width - 10
            )
            item_text_references.append((frame, text_ref))


window = Tk()
window.title("Inventory System")

window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)
notification_manager = EmailSender()
database_manager = DatabaseManager('../../database/database.db')

if not access_control.has_access_to('inventory'):
    messagebox.showerror("Access Denied", "You do not have permission to access the inventory page.")
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


def fetch_item_names():
    return db_manager.get_all_item_names()


def update_item_names(item_names):
    while len(item_names) < len(item_text_references):
        item_names.append("")

        # Update the text for each item on the canvas
    for text_ref, name in zip(item_text_references, item_names):
        canvas.itemconfig(text_ref, text=name)


def on_text_click(event):
    item_id = event.widget.find_withtag('current')[0]
    item_name = event.widget.itemcget(item_id, 'text')

    item_details = db_manager.get_item_description(item_name)
    message = f"Description: {item_details['description']}\n"
    message += f"Expiry Date: {item_details['expiry_date']}\n"
    message += f"Quantity: {item_details['quantity']}\n"
    message += f"Volume: {item_details['volume']}"

    messagebox.showinfo(f"Details of {item_name}", message)


item_text_references = []

item_positions = [
    (300.0, 460.0), (550.0, 460.0), (800.0, 460.0), (1050.0, 460.0),
    (300.0, 710.0), (550.0, 710.0), (800.0, 710.0), (1050.0, 710.0)
]

item_tags = ['Lemon', 'Chicken', 'Tomato', 'Egg', 'Milk']

item_names = fetch_item_names()

item_text_references = []
for position, tag in zip(item_positions, item_tags):
    text_ref = canvas.create_text(
        position[0], position[1],
        anchor="nw",
        text="",
        fill="#000000",
        font=("CutiveMono Regular", 27 * -1),
        tags=tag
    )
    item_text_references.append(text_ref)

for text_ref in item_text_references:
    canvas.tag_bind(text_ref, '<Button-1>', on_text_click)

update_item_names(item_tags)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    750.5,
    200.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=325.0,
    y=180.0,
    width=830.0,
    height=40.0
)

entry_1.bind('<Return>', search_items)

canvas.create_text(
    150.0,
    190.0,
    anchor="nw",
    text="Search:",
    fill="#000000",
    font=("CutiveMono Regular", 32 * -1)
)

canvas.create_text(
    18.0,
    20.0,
    anchor="nw",
    text="Welcome User",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    41.0,
    305.0,
    anchor="nw",
    text="List",
    fill="#000000",
    font=("CutiveMono Regular", 30 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [inventory_controller.next_page(), update_items_display()],
    relief="flat"
)
button_1.place(
    x=1198.0,
    y=524.0,
    width=100.0,
    height=100.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [inventory_controller.previous_page(), update_items_display()],
    relief="flat"
)
button_2.place(
    x=67.0,
    y=524.0,
    width=100.0,
    height=100.0
)


def create_item_labels(item_details):
    # Clear existing item labels
    for text_ref in item_text_references:
        canvas.delete(text_ref)
    item_text_references.clear()

    # Create and display new labels
    for index, item_detail in enumerate(item_details):
        if index >= len(item_positions):
            print("Warning: There are more items than positions defined.")
            break

        position = item_positions[index]

        # Create a frame around each item's details
        frame_width = 200
        frame_height = 150
        frame = canvas.create_rectangle(
            position[0] - frame_width / 2, position[1] - frame_height / 2,
            position[0] + frame_width / 2, position[1] + frame_height / 2,
            outline="#000000", width=2
        )

        display_text = (f"Name: {item_detail['foodName']}\n"
                        f"Desc: {item_detail['description'][:30]}\n"  # Truncate long descriptions
                        f"Exp: {item_detail['expiry_date']}\n"
                        f"Qty: {item_detail['quantity']}\n"
                        f"Vol: {item_detail['volume']}")

        text_ref = canvas.create_text(
            position[0], position[1],
            anchor="center",
            text=display_text,
            fill="#000000",
            font=("CutiveMono Regular", 14 * -1),
            width=frame_width - 10
        )
        item_text_references.append((frame, text_ref))


# Fetch and display all item details
all_item_details = inventory_controller.get_all_item_details()
create_item_labels(all_item_details)

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
    x=163.9996337890625,
    y=910.0000610351562,
    width=92.8746337890625,
    height=64.58258056640625
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: notification_manager.send_email(),
    relief="flat"
)
button_8.place(
    x=647.0,
    y=910.0,
    width=75.93649291992188,
    height=73.96893310546875
)

canvas.create_text(
    1088.0,
    988.69873046875,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_9.place(
    x=1155.109375,
    y=916.0,
    width=78.36550903320312,
    height=61.9512939453125
)

canvas.create_text(
    184.0,
    986.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    572.0,
    990.0,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

def on_gui_loaded():
    try:
        # Fetch low quantity items from the database
        low_quantity_items = database_manager.select_low_quantity_items('items', 'quantity')

        # Loop through each item
        if datetime.datetime.now().weekday() == 0:
            notification_manager.send_low_quantity_notification(low_quantity_items)

        messagebox.showinfo("Information", "Low quantity notification has been sent.")
        # Check for expiry alerts
        check_expiry_alerts()

    except Exception as e:
        print(f"Error during on_gui_loaded: {e}")


window.after(3000, on_gui_loaded)

window.resizable(False, False)
window.mainloop()
