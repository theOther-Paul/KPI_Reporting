import xlwings as xw

def header_text_look(worksheet1, arg1):
    """
    Apply a specific header style to a cell.

    This function sets the background color of the cell to a purple shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg1: The cell address (e.g., 'A1') as a string to apply the style to.

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> header_text_look(ws, 'A1')
    """
    worksheet1[arg1].color = (112, 48, 160)
    worksheet1.range(arg1).api.Font.Bold = True
    worksheet1.range(arg1).api.Font.ColorIndex = 2


def header2_text_look(worksheet1, arg1):
    """
    Apply a secondary header style to a cell.

    This function sets the background color of the cell to a blue shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg1: The cell address (e.g., 'A1') as a string to apply the style to.

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> header2_text_look(ws, 'A1')
    """
    worksheet1[arg1].color = (47, 117, 181)
    worksheet1.range(arg1).api.Font.Bold = True
    worksheet1.range(arg1).api.Font.ColorIndex = 2


def header3_text_look(worksheet1, arg1):
    """
    Apply a third header style to a cell.

    This function sets the background color of the cell to a green shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg1: The cell address (e.g., 'A1') as a string to apply the style to.

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> header3_text_look(ws, 'A1')
    """
    worksheet1[arg1].color = (0, 176, 80)
    worksheet1.range(arg1).api.Font.Bold = True
    worksheet1.range(arg1).api.Font.ColorIndex = 2


def adaptive_header1_style(worksheet1, arg1):
    """
    Apply an adaptive header style to a cell based on row and column indices.

    This function sets the background color of the cell to a purple shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg1: A tuple containing the row and column indices (e.g., (1, 1)).

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> adaptive_header1_style(ws, (1, 1))
    """
    worksheet1[arg1[1] - 1, arg1[0] - 1].color = (112, 48, 160)
    worksheet1[arg1[1] - 1, arg1[0] - 1].api.Font.Bold = True
    worksheet1[arg1[1] - 1, arg1[0] - 1].api.Font.ColorIndex = 2


def ci_count_style(worksheet1, arg1):
    """
    Apply a CI count style to a cell based on row and column indices.

    This function sets the background color of the cell to a dark blue shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg1: A tuple containing the row and column indices (e.g., (1, 1)).

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> ci_count_style(ws, (1, 1))
    """
    worksheet1[arg1[1] - 1, arg1[0] - 1].color = (0, 112, 192)
    worksheet1[arg1[1] - 1, arg1[0] - 1].api.Font.Bold = True
    worksheet1[arg1[1] - 1, arg1[0] - 1].api.Font.ColorIndex = 2


def adaptive_header2_style(worksheet1, arg_list):
    """
    Apply an adaptive header style to a cell based on row and column indices.

    This function sets the background color of the cell to a blue shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg_list: A list containing the row and column indices (e.g., [1, 1]).

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> adaptive_header2_style(ws, [1, 1])
    """
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].color = (47, 117, 181)
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.Bold = True
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.ColorIndex = 2


def adaptive_header3_style(worksheet1, arg_list):
    """
    Apply an adaptive header style to a cell based on row and column indices.

    This function sets the background color of the cell to a green shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg_list: A list containing the row and column indices (e.g., [1, 1]).

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> adaptive_header3_style(ws, [1, 1])
    """
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].color = (0, 176, 80)
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.Bold = True
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.ColorIndex = 2


def adaptive_ci_header_style(worksheet1, arg_list):
    """
    Apply a CI header style to a cell based on row and column indices.

    This function sets the background color of the cell to a gray-blue shade,
    makes the font bold, and sets the font color to white.

    :param worksheet1: The worksheet object where the styling will be applied.
    :param arg_list: A list containing the row and column indices (e.g., [1, 1]).

    :example:
    >>> import xlwings as xw
    >>> wb = xw.Book()
    >>> ws = wb.sheets['Sheet1']
    >>> adaptive_ci_header_style(ws, [1, 1])
    """
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].color = (68, 84, 106)
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.Bold = True
    worksheet1[arg_list[1] - 1, arg_list[0] - 1].api.Font.ColorIndex = 2
