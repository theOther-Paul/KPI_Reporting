from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .headers import movements
from .headers import helper as helper
from .headers import visuals as visuals
from collections import ChainMap
from PIL import Image
import matplotlib.pyplot as plt

l = helper.GrabLogs()
df = helper.assign_lt()


# The ToolTip class creates a tooltip window that displays text when the user hovers over a widget.
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            tw,
            text=self.text,
            justify=LEFT,
            background="#ffff88",
            relief=SOLID,
            borderwidth=1,
            font=("montserrat", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    """
    This function creates a tooltip for a given widget in Python.

    :param widget: The widget for which the tooltip is being created. This can be any tkinter widget
    such as a button, label, or entry field
    :param text: The text that will be displayed in the tooltip when the user hovers over the widget
    """
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


def option_function_dict(df, home_function):
    """
    The function creates a dictionary of options and their corresponding functions to be used in a
    visualization tool.

    :param df: a pandas DataFrame containing the data to be used for generating the options
    :param home_function: It is a string parameter representing the home_function for which the data is being analyzed
    :return: The function `option_function_dict` returns a dictionary `opt_func_dict` containing keys
    representing different options and values representing the corresponding functions to be called for
    each option.
    """
    k = visuals.FormTable(df, home_function)
    return {
        "MB-1 name list": k.gen_mb1,
        "RLFT name list": k.gen_rlft,
        "Cross industry names list": k.gen_cross_ind,
        "US Nationals": k.gen_us_nationals,
        "Cross  Industry Names": k.gen_cross_ind,
        "Placeholder": None,
    }


def option1_function_dict(df, home_function):
    k = visuals.FormTable(df, home_function)
    return {
        "Total MB population (%)": k.gen_population,
        "Female (%) in Senior Teams": k.gen_female_srt,
        "Female G34+": k.gen_fem34,
    }


def column_list(df):
    """
    The function returns a list of column names from a pandas DataFrame.

    :param df: A pandas DataFrame object
    :return: a list of column names from a pandas DataFrame.
    """
    return list(df)


def display_df(root, option):
    """
    This function displays a pandas dataframe in a GUI table using the pandastable library.

    :param root: The root parameter is the tkinter root window where the table will be displayed
    :param option: The parameter "option" is a pandas DataFrame that contains the data to be displayed
    in the table
    """
    from pandastable import Table

    table = pt = Table(
        root,
        dataframe=option,
        showtoolbar=True,
        showstatusbar=True,
        sortable=True,  # Enable sorting
        editable=True,  # Allow editing (note: changes won't be saved to the original dataframe)
        resizable=True,  # Allow column resizing
        showindex=False,  # Hide the DataFrame index column
        selectionmode="extended",  # Enable multiple row selection with Ctrl/Shift
    )
    pt.show()
    l.form_log(f"Dataframe displayed for {option}", 20)


def data_vis(root):
    """
    This function creates a GUI window for viewing and selecting data options, including a combobox for
    selecting a LT and another for selecting an option to display in tabular form.

    :param root: The root window of the tkinter GUI application
    """
    window = Toplevel(root)
    window.wm_title("View your data")
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
        text="Back to prev",
        command=lambda: ex_onclick(),
    )
    exbtn.grid(row=1, column=0)

    banner = ttk.Label(
        window, text="View your data", font=("Montserrat", 20), anchor="n"
    )
    banner.grid(row=2, column=0, columnspan=2)

    # select data - LT section
    lt1_label = ttk.Label(
        window, text="Select LT from list", font=("Montserrat", 12), anchor="n"
    )
    CreateToolTip(
        lt1_label,
        text="By selecting the desired LT for viewing the data, \n and then clicking the 'Downoad' button, \n a filtered data file will be downloaded \nand opened for viewing",
    )
    lt1_label.grid(row=4, column=0, sticky=W, padx=5, pady=3)
    current_var = tk.StringVar()
    combobox = ttk.Combobox(
        window, textvariable=current_var, width=24, font=("Montserrat 12")
    )
    if helper.generate_combo() is [] or None:
        combobox["values"] = ""
    else:
        combobox["values"] = helper.generate_combo()
    combobox["state"] = "readonly"
    combobox.grid(row=5, column=0, sticky=N, padx=5, pady=3)

    # view data - Available options for display
    sect_label = ttk.Label(
        window, text="Select an option to display", font=("Montserrat 12"), anchor="n"
    )
    CreateToolTip(
        sect_label,
        text="You can choose only one option to be displayed below. \n Each option will be displayed in a tabular form, for better visualization. \n All options from the list will display data for the actual quarter",
    )

    sect_label.grid(row=6, column=0, sticky=W, padx=5, pady=3)
    current1_var = tk.StringVar()

    opt_val = ChainMap(
        option_function_dict(df, combobox.get()),
        option1_function_dict(df, combobox.get()),
        # option_w_revargs_function_dict(combobox.get(), df),
    )
    opt_combobox = ttk.Combobox(
        window,
        values=list(opt_val),
        width=24,
        font=("Montserrat 12"),
        justify="center",
        textvariable=current1_var,
    )
    opt_combobox["state"] = "readonly"
    opt_combobox.grid(row=7, column=0, sticky=N, padx=5, pady=3)

    def com_display_df():
        dicto = option_function_dict(
            helper.filter_by_quarter(q_combobox.get()), combobox.get()
        )
        dicto1 = option1_function_dict(
            helper.filter_by_quarter(q_combobox.get()), combobox.get()
        )
        res_dict = ChainMap(dicto, dicto1)
        try:
            display_df(
                Toplevel(window),
                res_dict[opt_combobox.get()](),
            )
        except Exception:
            try:
                display_df(
                    Toplevel(window), res_dict[opt_combobox.get()](q_combobox.get())
                )
            except Exception:
                display_df(
                    Toplevel(window),
                    res_dict[opt_combobox.get()](q_combobox.get(), helper.assign_lt()),
                )

    # quarter combo box assembly
    q_list_label = ttk.Label(
        window, text="Select Quarter", font=("Montserrat 12"), anchor="n"
    )
    q_list_label.grid(row=8, column=0, sticky=W, padx=5, pady=3)
    q_var = tk.StringVar()
    q_combobox = ttk.Combobox(
        window,
        values=list(helper.get_quarter_month_list()),
        width=24,
        font=("Montserrat 12"),
        justify="center",
        textvariable=q_var,
    )
    q_combobox["state"] = "readonly"
    q_combobox.grid(row=9, column=0, sticky=N, padx=5, pady=3)

    ttk.Button(
        window,
        text="Show",
        style="standard.TButton",
        command=lambda: com_display_df(),
    ).grid(row=10, column=0, pady=5, padx=5)
