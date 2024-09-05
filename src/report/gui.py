import os
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, messagebox
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
from src.utilities.window_manager import WindowManager
from src.utilities.notification_manager import EmailSender
from src.report.report import HealthAndSafetyLogic
from src.utilities.expiry_log import expiry_logger
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/report")
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)
notification_manager = EmailSender()

if not access_control.has_access_to('report'):
    messagebox.showerror("Access Denied", "You do not have permission to access the report page.")
    window_manager.run_new_file('gui2')
    exit()
expiry_logger()
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
    72.0,
    5.0,
    anchor="nw",
    text="Health And Safety Report",
    fill="#000000",
    font=("CutiveMono Regular", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    685.5,
    433.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=188.0,
    y=145.0,
    width=995.0,
    height=574.0
)

canvas.create_text(
    183.0,
    106.0,
    anchor="nw",
    text="Preview",
    fill="#000000",
    font=("CutiveMono Regular", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: health_and_safety_logic.display_user_access_logs(),
    relief="flat"
)
button_1.place(
    x=222.0,
    y=731.0,
    width=437.6451416015625,
    height=72.65625
)

health_and_safety_logic = HealthAndSafetyLogic(window_manager, access_control, db_manager, notification_manager,
                                               entry_1)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: health_and_safety_logic.generate_and_send_pdf(entry_1.get("1.0", "end-1c")),
    relief="flat"
)
button_2.place(
    x=707.3548583984375,
    y=733.34375,
    width=437.6451416015625,
    height=72.65625
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
    x=154.9996337890625,
    y=897.0000610351562,
    width=92.8746337890625,
    height=64.58258056640625
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
    x=638.0,
    y=897.0,
    width=75.93649291992188,
    height=73.96893310546875
)

canvas.create_text(
    1079.0,
    975.6986083984375,
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
    x=1146.109375,
    y=903.0,
    width=78.36550903320312,
    height=61.9512939453125
)

canvas.create_text(
    175.0,
    973.0,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

canvas.create_text(
    563.0,
    977.0,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)
window.resizable(False, False)
window.mainloop()
