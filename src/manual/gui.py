from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Entry, messagebox
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from src.utilities.window_manager import WindowManager
from manual import ManualEntry
from src.utilities.notification_manager import EmailSender
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/manual")
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


ManualEntry = ManualEntry()

window = Tk()

window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)
notification_manager = EmailSender()

if not access_control.has_access_to('manual'):
    messagebox.showerror("Access Denied", "You do not have permission to access the manual entry page.")
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
canvas.create_text(
    43.0,
    4.0,
    anchor="nw",
    text="Enter Food Details",
    fill="#000000",
    font=("CutiveMono Regular", 32 * -1)
)

canvas.create_text(
    46.0,
    129.0,
    anchor="nw",
    text="Food Name:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    48.0,
    293.0,
    anchor="nw",
    text="Food Description:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    887.0,
    146.0,
    anchor="nw",
    text="Expiry Date:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    893.0,
    312.0,
    anchor="nw",
    text="Quantity:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    408.5,
    220.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=46.0,
    y=183.0,
    width=725.0,
    height=72.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    417.5,
    477.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=50.0,
    y=342.0,
    width=735.0,
    height=268.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    1078.5,
    234.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=889.0,
    y=197.0,
    width=379.0,
    height=72.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    1013.5,
    399.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    validate="key",
    validatecommand=(window.register(lambda char: char.isdigit() or char == ""), '%S')
)
entry_4.place(
    x=892.0,
    y=362.0,
    width=243.0,
    height=73.0
)
entry_4.insert(0, '1')

canvas.create_text(
    893.0,
    480.0,
    anchor="nw",
    text="Volume:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_5 = canvas.create_image(
    1013.5,
    579.5,
    image=entry_image_4
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=892.0,
    y=542.0,
    width=243.0,
    height=73.0
)
entry_5.insert(0, '1')

# Add item button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ManualEntry.submit_entry_gui(entry_1, entry_2, entry_3, entry_4, entry_5),
    relief="flat"
)
button_1.place(
    x=100.0,
    y=697.0,
    width=325.0,
    height=72.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ManualEntry.read_qr(entry_1, entry_2, entry_3, entry_5),
    relief="flat"
)
button_7.place(
    x=523.0,
    y=697.0,
    width=325.0,
    height=72.0
)

# View added items button
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui11'),
    relief="flat"
)
button_8.place(
    x=950.0,
    y=697.0,
    width=325.0,
    height=72.0
)

# Decrease quantity button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))

button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ManualEntry.decrease_quantity(entry_4),
    relief="flat"
)
button_2.place(
    x=1102.0,
    y=400.0,
    width=20.0,
    height=26.0
)

# Increase quantity button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ManualEntry.increase_quantity(entry_4),
    relief="flat"
)
button_3.place(
    x=1102.0,
    y=374.0,
    width=20.0,
    height=32.0
)

# Back button
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
    x=153.9996337890625,
    y=898.0000305175781,
    width=92.87466430664062,
    height=64.5826416015625
)

# Call assistance button
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: notification_manager.send_email(),
    relief="flat"
)
button_5.place(
    x=637.0,
    y=898.0,
    width=75.93650817871094,
    height=73.96893310546875
)

canvas.create_text(
    1078.0,
    976.6986083984375,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

# Logout button
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_6.place(
    x=1145.109375,
    y=904.0,
    width=78.365478515625,
    height=61.951263427734375
)

canvas.create_text(
    174.0,
    974.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    562.0,
    978.0,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)
window.resizable(False, False)
window.mainloop()
