from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from .headers import helper
from .headers import emailer
from . import pages
import subprocess
import os

hrbp_temp = emailer.get_mail_details()


def isBlank(myString):
    return not (myString and myString.strip())


def isNotBlank(myString):
    return bool(myString and myString.strip())


def ask_change_structure(file_loc="mapping/mblt_map.xlsx"):
    file_gen = os.path.join(os.getcwd(), file_loc).replace("\\", "\\")
    if prompt := messagebox.askokcancel(
        title="Modify Current LT Structure",
        message="To modify the current organizational structure, it's necessary to modify the mapping tables."
        "\n Currently, this operation is not supported by the interface."
        "\n Would you like to proceed?",
    ):
        return subprocess.call(
            [file_gen],
            shell=True,
        )


def change_LT(root):
    window = Toplevel(root)
    window.wm_title("Settings")

    # icons
    wi1 = PhotoImage(file="pages/assets/icon1.ico")
    window.iconphoto(False, wi1)

    def ex_onclick():
        window.grab_release()
        window.destroy()

    def on_configure(event):
        # Update the scroll region to cover the entire window
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Calculate the required size based on the content and add some padding
        width = frame.winfo_reqwidth() + 30
        height = frame.winfo_reqheight() + 30
        window.maxsize(width, height)
        window.minsize(int(width), int(height) // 2)

    def on_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    # Canvas widget to contain the frame with scrollable content
    canvas = Canvas(window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    canvas.bind("<MouseWheel>", on_mousewheel)

    # Scrollbar for the canvas
    scrollbar = Scrollbar(window, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", on_configure)

    # Frame to hold the content
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    btn_style = ttk.Style()
    btn_style.configure("standard.TButton", font=("Montserrat", 12))
    exbtn = ttk.Button(
        frame,
        style="standard.TButton",
        text="←",
        width=1,
        command=ex_onclick,
    )
    exbtn.grid(row=0, column=0, sticky="w")

    # Settings banner
    ttk.Label(frame, text="Change LT/MB Settings", font=("Montserrat 22")).grid(
        row=2, column=1, columnspan=4, rowspan=2
    )
    r = 4

    mbdf = helper.get_mblt_func()
    mbdf.drop_duplicates(subset="MBSharedResponsibility2").dropna()

    for k, v in mbdf.iterrows():
        ttk.Label(frame, text="┊", font=("Montserrat 12")).grid(row=r, column=0)
        ttk.Label(
            frame, text=f"{v['MBSharedResponsibility2']}", font=("Montserrat 12")
        ).grid(row=r, column=1)
        ttk.Label(frame, text="┊", font=("Montserrat 12")).grid(row=r, column=2)
        ttk.Label(frame, text=f"{v['LT - Functional']}", font=("Montserrat 12")).grid(
            row=r, column=3
        )
        ttk.Label(frame, text="┊", font=("Montserrat 12")).grid(row=r, column=4)
        r += 1

    new_btn = ttk.Button(
        frame,
        text="Add New Entry",
        style="standard.TButton",
        command=lambda: ask_change_structure(),
    )
    pages.CreateToolTip(
        new_btn,
        "Adds a new entry to the MB - LT mapping table. \n It's recommended to fill both fields",
    )
    sep = ttk.Separator(frame, orient="horizontal")
    sep.grid(row=r, column=0, columnspan=5, sticky="ew", pady=15, padx=10)
    new_btn.grid(row=r + 1, column=3, pady=4)

    # Update the canvas scroll region when the frame size changes
    frame.bind("<Configure>", on_configure)

    # Initially trigger on_configure to set the initial size
    on_configure(None)


def change_HRBP(root):
    window = Toplevel(root)
    window.wm_title("Settings")
    window.grab_set()

    # icons
    wi1 = PhotoImage(file="pages/assets/icon1.ico")
    window.iconphoto(False, wi1)

    def ex_onclick():
        window.grab_release()
        window.destroy()

    btn_style = ttk.Style()
    btn_style.configure("standard.TButton", font=("Montserrat", 12))
    exbtn = ttk.Button(
        window,
        style="standard.TButton",
        text="←",
        width=1,
        command=lambda: ex_onclick(),
    )
    pages.CreateToolTip(exbtn, "Back to previous page")
    exbtn.grid(row=0, column=0)

    # Settings banner
    ttk.Label(
        window, text="Change Current HRBP List Settings", font=("Montserrat 22")
    ).grid(row=2, column=3, columnspan=3)
    temp_list = []
    r = 5
    for idx, col in hrbp_temp.iterrows():
        ttk.Label(window, text="┊", font=("Montserrat 12")).grid(row=r, column=0)
        ttk.Label(window, text=f"{col['HRBP']}", font=("Montserrat 12")).grid(
            row=r, column=1
        )
        ttk.Label(window, text="┊", font=("Montserrat 12")).grid(row=r, column=2)
        ttk.Label(window, text=f"{col['HRBP Mail']}", font=("Montserrat 12")).grid(
            row=r, column=3
        )
        ttk.Label(window, text="┊", font=("Montserrat 12")).grid(row=r, column=4)
        ttk.Label(window, text=f"{col['LT']}", font=("Montserrat 12")).grid(
            row=r, column=5
        )
        ttk.Button(
            window,
            text="Change",
            style="standard.TButton",
            command=lambda: ask_change_structure(
                file_loc="mapping/HRBP_mailing_list.xlsx"
            ),
        ).grid(row=r, column=6, pady=1, padx=2)
        r += 1
    new_btn = ttk.Button(
        window,
        text="Add New Entry",
        style="standard.TButton",
        command=lambda: ask_change_structure(),
    )
    pages.CreateToolTip(
        new_btn,
        "Adds a new entry to the MB - LT mapping table. \n It's recomended to fill both fields",
    )
    new_btn.grid(row=r, column=6, pady=10, padx=10)
