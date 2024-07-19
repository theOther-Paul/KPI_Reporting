import flet as ft
from logs.logger_class import GrabLogs
from headers import file_ops, visuals, consolidate, kpi
import pandas as pd


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

        # combobox and dropdowns
        self.raw_drop = consolidate.GatherData().form_combo()

        self.dropdown_var = None

        self.dropdown = ft.Dropdown(
            hint_text="Choose a department",
            width=200,
            options=[ft.dropdown.Option(value) for value in self.raw_drop],
            on_change=self.drop_changed,
        )

        self.empty_text_label = ft.Text()

        self.df = file_ops.FilePrep().split_by_snap()[1]

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
        self.show_home()

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

    def drop_changed(self, e):
        """
        Update the selected dropdown value, update the empty text label, and trigger DataTable update.

        Parameters:
        - e: Event object containing information about the dropdown selection change.
        """
        self.dropdown_var = e.control.value  # Update the selected dropdown value
        self.empty_text_label.value = (
            f"Selected Value: {self.dropdown_var}"  # Update the text label
        )

        self.update_table()

    def update_table(self):
        """
        Filter data based on the dropdown selection and update the DataTable.
        """
        df_filtered = (
            self.df[self.df["department"] == self.dropdown_var]
            if self.dropdown_var
            else self.df
        )  # Filter data based on dropdown selection

        df_to_convert = kpi.EmployeeAnalytics(
            df_filtered, self.empty_text_label
        ).form_df()

        gender_table_columns, gender_table_rows = consolidate.create_flet_table(
            df_to_convert
        )

        self.content.controls = [
            ft.Text("Welcome to the KPI Reporting App"),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Combobox section"),
                                    self.dropdown,
                                    self.empty_text_label,
                                ]
                            ),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREEN_200,
                            width=350,
                            height=150,
                            border_radius=10,
                        ),
                        ft.DataTable(
                            bgcolor="green",
                            horizontal_lines=ft.BorderSide(1, "blue"),
                            heading_row_color=ft.colors.BLACK12,
                            heading_row_height=25,
                            data_row_color={"hovered": "0x30FF0000"},
                            column_spacing=25,
                            columns=[
                                ft.DataColumn(ft.Text(column))
                                for column in gender_table_columns
                            ],
                            rows=gender_table_rows,
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

    def show_home(self):
        """
        Set up the home page content with a dropdown menu, a text label, and a data table,
        and update the page with the new content.
        """
        self.empty_text_label = ft.Text()
        self.update_table()

    def show_plot(self, e):

        self.content.controls = [
            ft.Column(
                [
                    ft.Text("Plotting Section examples"),
                    ft.Row(
                        [
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
                            ft.Container(
                                content=visuals.show_line(),
                                margin=10,
                                padding=10,
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.BLUE_500,
                                width=500,
                                height=500,
                                border_radius=10,
                            ),
                        ]
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
            action()
