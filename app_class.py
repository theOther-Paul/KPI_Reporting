import flet as ft
from logs.logger_class import GrabLogs
from headers import file_ops, visuals
import pandas as pd
from flet.matplotlib_chart import MatplotlibChart


# The `AppFace` class creates a simple app interface with a sidebar navigation rail and content area
class AppFace:
    logger = GrabLogs().configure_logger("main.log")

    def __init__(self, page):
        """
        The function initializes a page with a title, horizontal alignment, sidebar, and main content
        area layout.

        :param page: The `page` parameter in the `__init__` method is used to initialize a page object.
        In this code snippet, the `page` object seems to be a part of a user interface framework
        (possibly `ft` module) and is being customized with specific attributes like title and
        horizontal alignment
        """

        self.page = page
        self.page.title = "KPI Reporting v.01"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Add the filepicker to the page
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        self.file_output = ft.Text(value="No File Selected")

        # Initialize sidebar and content area
        self.sidebar = self.create_sidebar()
        self.content = ft.Column(controls=[ft.Text("Welcome to the app!")], expand=True)

        # Layout with sidebar and main content
        self.page.add(
            ft.Row(
                controls=[
                    ft.Container(content=self.sidebar, width=150),
                    ft.VerticalDivider(width=1),
                    self.content,
                ],
                expand=True,
            )
        )

    def create_sidebar(self):
        """
        The function `create_sidebar` generates a navigation rail with specific properties and
        destinations.
        :return: The `create_sidebar` function is returning a navigation rail component with a logo,
        three navigation destinations (Home, Profile, Settings), and an `on_change` event handler.
        """
        # Add navigation rail
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            leading=ft.Image(
                src=f"assets/comp_logo.jpg",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME_FILLED,
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.TABLE_CHART_SHARP,
                    selected_icon=ft.icons.TABLE_VIEW_SHARP,
                    label="Reports",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SCATTER_PLOT_OUTLINED,
                    selected_icon=ft.icons.SCATTER_PLOT_SHARP,
                    label="Show Data",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS_SHARP,
                    label="Settings",
                ),
            ],
            on_change=self.on_nav_change,
            expand=True,
        )

        popup_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    text="Light Theme",
                    on_click=lambda e: self.change_theme(ft.ThemeMode.LIGHT),
                ),
                ft.PopupMenuItem(
                    text="Dark Theme",
                    on_click=lambda e: self.change_theme(ft.ThemeMode.DARK),
                ),
                ft.PopupMenuItem(
                    text="System Default",
                    on_click=lambda e: self.change_theme(ft.ThemeMode.SYSTEM),
                ),
            ],
            icon=ft.icons.DARK_MODE_OUTLINED,
        )

        return ft.Column(
            controls=[
                rail,
                ft.Container(
                    content=popup_menu, alignment=ft.alignment.center, margin=10
                ),
            ],
            expand=True,
        )

    def create_file_picker(self, e=None):
        self.file_picker.pick_files(allowed_extensions=["csv", "xlsx"])

    def on_file_selected(self, e):
        if e.files:
            file_path = e.files[0].path
            self.file_output.value = f"Selected file: {file_path}"
            self.page.update()

            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                self.file_output.value = "Unsupported file type"
                self.page.update()
                return

            # Pass the DataFrame to the external function
            self.process_data_frame(df)

    def process_data_frame(self, df):
        print("Appending in")
        container = file_ops.FilePrep()._append_to_df(df)
        print("Appending done. wait for the confirmation message")

        self.show_confimation(
            "Upload Successful",
            "Chosen file have been successfully uploaded to the base file",
        )

    def show_confimation(self, title, message):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: None,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_confirmation_modal(self, title, message):
        def confirm(e):
            dialog.open = False
            self.page.update()
            print("Modal dialog closed (user selected 'Yes')")

        def cancel(e):
            dialog.open = False
            self.page.update()
            print("Modal dialog closed (user selected 'Cancel')")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Are you sure you want to delete this file?"),
            actions=[
                ft.TextButton("Yes", on_click=confirm),
                ft.TextButton("Cancel", on_click=cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_home(self, e):
        self.content.controls = [
            ft.Text("Welcome to the KPI Reporting App"),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Combobox section"),
                                    ft.Dropdown(
                                        width=100,
                                        options=[
                                            ft.dropdown.Option("Red"),
                                            ft.dropdown.Option("Red1"),
                                            ft.dropdown.Option("Red2"),
                                        ],
                                    ),
                                ]
                            ),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREEN_200,
                            width=150,
                            height=150,
                            border_radius=10,
                        ),
                        ft.Text(),
                        ft.DataTable(
                            width=700,
                            bgcolor="green",
                            border=ft.border.all(2, "red"),
                            border_radius=10,
                            vertical_lines=ft.BorderSide(3, "blue"),
                            horizontal_lines=ft.BorderSide(1, "green"),
                            sort_column_index=0,
                            sort_ascending=True,
                            heading_row_color=ft.colors.BLACK12,
                            heading_row_height=100,
                            data_row_color={"hovered": "0x30FF0000"},
                            show_checkbox_column=True,
                            divider_thickness=0,
                            column_spacing=200,
                            columns=[
                                ft.DataColumn(ft.Text("First name")),
                                ft.DataColumn(ft.Text("Last name")),
                                ft.DataColumn(ft.Text("Age"), numeric=True),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("John")),
                                        ft.DataCell(ft.Text("Smith")),
                                        ft.DataCell(ft.Text("43")),
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Jack")),
                                        ft.DataCell(ft.Text("Brown")),
                                        ft.DataCell(ft.Text("19")),
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Alice")),
                                        ft.DataCell(ft.Text("Wong")),
                                        ft.DataCell(ft.Text("25")),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                margin=9,
                padding=9,
                alignment=ft.alignment.center_left,
                bgcolor=ft.colors.AMBER_400,
                height=300,
                border_radius=10,
            ),
        ]
        self.page.update()

    def show_report_downloader(self, e):
        self.content.controls = [
            ft.Text("This Section is used to check data and download reports"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Raw Data File Section"),
                        ft.FilledButton(
                            text="Open Raw Data",
                            on_click=lambda e: file_ops.FilePrep().open_raw_data(),
                            tooltip="Opens the raw data file",
                        ),
                    ],
                ),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREEN,
                width=200,
                height=150,
                border_radius=10,
            ),
            ft.Text("This section is destined for uploading new file to the database"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Upload File Section"),
                        ft.FilledButton(
                            text="Upload new file",
                            icon=ft.icons.UPLOAD_FILE,
                            tooltip="Choose a file to upload to the Database",
                            # on_click=self.create_file_picker,
                            on_click=lambda _: self.show_confimation(
                                "Upload Successful",
                                "The file has been successfully uploaded intop the central file. \nPress anywhere to dismiss this prompt",
                            ),
                        ),
                    ]
                ),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_500,
                width=200,
                height=150,
                border_radius=10,
            ),
        ]

        self.page.update()

    def show_plot(self, e):

        self.content.controls = [
            ft.Column(
                [
                    ft.Text("Plotting Section example"),
                    ft.Container(
                        content=visuals.show_fruits(),
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.BLUE_300,
                        width=500,
                        height=500,
                        border_radius=10,
                    ),
                ]
            )
        ]

        self.page.update()

    def show_settings(self, e):
        self.content.controls = [
            ft.Text("Settings"),
            ft.Text("Clear logs"),
            ft.OutlinedButton(
                text="Clear all current log files",
                on_click=lambda: self.logger.clear_logs(),
            ),
        ]
        self.page.update()

    def check_item_clicked(self, param):
        param.control.checked = not param.control.checked
        self.page.update()

    def change_theme(self, theme_mode: ft.ThemeMode):
        self.page.theme_mode = theme_mode
        self.page.update()
        self.logger.log("info", f"Theme changed to {theme_mode}")

    def on_nav_change(self, e):
        """
        The function `on_nav_change` takes an event `e` and based on the selected index, it calls a
        corresponding action method.

        :param e: The `e` parameter in the `on_nav_change` function likely represents an event object
        that contains information about the navigation change event that occurred. This object may
        include details such as the control that triggered the event and any relevant data associated
        with the event.
        """
        selected_index = e.control.selected_index
        actions = {
            0: self.show_home,
            1: self.show_report_downloader,
            2: self.show_plot,
            3: self.show_settings,
            4: self.change_theme,
        }

        action = actions.get(selected_index)
        if action:
            action(e)
