from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from src.utilities.window_manager import WindowManager
from login import LoginSystem
import logging

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../../img/login")
# Configure logging
logging.basicConfig(filename='../utilities/system.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
 

window = Tk()

window.geometry("1366x1024")
window.configure(bg="#FFFFFF")

window_manager = WindowManager(window)


def handle_login():
    global entry_1, entry_2
    try:
        login_system = LoginSystem('../../database/database.db')
        login_system.handle_login(entry_1, entry_2, window_manager)
    except Exception as e:
        logging.error(f"Login error: {e}")
        messagebox.showerror("Login Error", "An unexpected error occurred during login.")


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
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    818.0282592773438,
    576.9846878051758,
    image=entry_image_1
)
entry_1 = Entry(  # USERNAME
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=439.0,
    y=546.0,
    width=758.0565185546875,
    height=59.96937561035156
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    818.0334167480469,
    672.9526290893555,
    image=entry_image_2
)
entry_2 = Entry(  # PASSWORD
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*",
)
entry_2.place(
    x=439.0,
    y=642.0000610351562,
    width=758.0668334960938,
    height=59.90513610839844
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    686.8068237304688,
    234.26934814453125,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    648.0,
    263.0,
    image=image_image_2
)

canvas.create_text(
    169.024169921875,
    558.9999389648438,
    anchor="nw",
    text="USERNAME",
    fill="#000000",
    font=("CutiveMono Regular", 32 * -1)
)

canvas.create_text(
    169.0,
    655.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=("CutiveMono Regular", 32 * -1)
)

canvas.create_text(
    101.0,
    60.0,
    anchor="nw",
    text="FFSMART \nFRIDGE",
    fill="#000000",
    font=("CutiveMono Regular", 36 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(  # LOGIN BUTTON
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=handle_login,
    relief="flat",
)
button_1.place(
    x=308.8934020996094,
    y=810.6857604980469,
    width=748.1900634765625,
    height=71.12179565429688
)
window.resizable(False, False)
window.mainloop()
