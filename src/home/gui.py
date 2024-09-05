from pathlib import Path
from src.utilities.window_manager import WindowManager
from src.utilities.notification_manager import EmailSender
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from src.utilities.access_control import AccessControl
from src.utilities.database_manager import DatabaseManager
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/home")
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)
notification_manager = EmailSender()
db_manager = DatabaseManager('../../database/database.db')
access_control = AccessControl(db_manager)

if not access_control.has_access_to('home'):
    messagebox.showerror("Access Denied", "You do not have permission to access the home page.")
    window_manager.run_new_file('gui4')
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
    89.0,
    36.0,
    anchor="nw",
    text="Home",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui5'),
    relief="flat"
)
button_1.place(
    x=214.115234375,
    y=167.0,
    width=952.4088745117188,
    height=91.91073608398438
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui7'),
    relief="flat"
)
button_2.place(
    x=214.115234375,
    y=290.1569519042969,
    width=952.4088745117188,
    height=91.91072845458984
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui9'),
    relief="flat"
)
button_3.place(
    x=214.115234375,
    y=532.2405395507812,
    width=952.4088745117188,
    height=91.91073608398438
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
    x=637,
    y=881.0,
    width=75.93650817871094,
    height=73.96893310546875
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    890.998046875,
    1265.6903076171875,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    918.30908203125,
    1266.6658935546875,
    image=image_image_2
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui3'),
    relief="flat"
)
button_5.place(
    x=214.115234375,
    y=411.0,
    width=952.4088745117188,
    height=91.91072845458984
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui8'),
    relief="flat"
)
button_8.place(
    x=214.115234375,
    y=654.0,
    width=952.4088745117188,
    height=91.91072845458984
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    1235.1103515625,
    917.0,
    image=image_image_3
)

canvas.create_text(
    584.0,
    959.0,
    anchor="nw",
    text="Call Assistance",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window_manager.run_new_file('gui2'),
    relief="flat"
)
button_6.place(
    x=86.9996337890625,
    y=886.0000305175781,
    width=92.87466430664062,
    height=64.5826416015625
)

canvas.create_text(
    1185.0,
    958.721435546875,
    anchor="nw",
    text="Log Out",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [access_control.end_session(), window_manager.run_new_file('gui4')],
    relief="flat"
)
button_7.place(
    x=1212.1103515625,
    y=887.0,
    width=78.365478515625,
    height=61.951263427734375
)

canvas.create_text(
    106.9993896484375,
    960.9999389648438,
    anchor="nw",
    text="Back",
    fill="#000000",
    font=("CutiveMono Regular", 26 * -1)
)
window.resizable(False, False)
window.mainloop()
