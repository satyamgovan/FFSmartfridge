from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from src.utilities.window_manager import WindowManager
from src.utilities.notification_manager import EmailSender
from remove import RemoveItem
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/remove")
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


RemoveItem = RemoveItem()

window = Tk()

window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)
notification_manager = EmailSender()
if not access_control.has_access_to('remove'):
    messagebox.showerror("Access Denied", "You do not have permission to access the remove items page.")
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
    63.0,
    18.0,
    anchor="nw",
    text="Remove Items",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

canvas.create_text(
    117.0,
    173.0,
    anchor="nw",
    text="Item Code:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    426.0,
    275.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=116.0,
    y=243.0,
    width=620.0,
    height=62.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: RemoveItem.removeFoodGui(entry_1,entry_2),
    relief="flat"
)
button_1.place(
    x=115.00030517578125,
    y=539.9999904632568,
    width=391.42742919921875,
    height=70.97403717041016
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui3'),
    relief="flat"
)
button_2.place(
    x=246.0,
    y=727.0,
    width=874.0,
    height=72.0
)

canvas.create_text(
    63.0,
    1295.20361328125,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    404.87890625,
    1304.8448486328125,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    800.677734375,
    1304.1260986328125,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    890.787109375,
    1261.427490234375,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    918.09765625,
    1262.403076171875,
    image=image_image_2
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_3.place(
    x=101.9996337890625,
    y=903.0000305175781,
    width=92.87466430664062,
    height=64.5826416015625
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: notification_manager.send_email(),
    relief="flat"
)
button_4.place(
    x=645.0,
    y=898.0,
    width=75.93650817871094,
    height=73.96893310546875
)

canvas.create_text(
    1125.0,
    976.6986083984375,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    116.0,
    976.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    576.0,
    976.9999389648438,
    anchor="nw",
    text="Call Assistance",
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
    x=1197.0,
    y=910.0,
    width=78.365478515625,
    height=61.951263427734375
)

canvas.create_text(
    115.0,
    361.0,
    anchor="nw",
    text="Quantity:",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    235.5,
    448.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=114.0,
    y=411.0,
    width=243.0,
    height=73.0
)

window.resizable(False, False)
window.mainloop()