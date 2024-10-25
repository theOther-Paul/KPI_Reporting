import flet as ft
from headers.kpi import kpi_department, kpi_market, report_builder
from logs.logger_class import GrabLogs
from headers import file_ops, visuals, consolidate
import pandas as pd
import threading


# The `AppFace` class creates a simple app interface with a sidebar navigation rail and content area
class AppFace:
    logger = GrabLogs().configure_logger("main.log")

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "KPI Reporting v.01"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.default_width = self.page.width
        self.default_height = self.page.height

        self.modified_width = 0

        # Add the file picker to the page
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        self.file_output = ft.Text(value="No File Selected")

        # Initialize sidebar and content area
        self.sidebar = self.create_sidebar()
        self.content = ft.Column(controls=[], expand=True)

        # ComboBox and dropdowns for home page
        self.dpt_raw_drop = consolidate.GatherData().form_combo("department")
        self.dpt_dropdown_var = None

        self.mkt_raw_drop = consolidate.GatherData().form_combo("market")
        self.mkt_dropdown_var = None

        self.department_dropdown = ft.Dropdown(
            hint_text="Choose a department",
            width=200,
            options=[ft.dropdown.Option(value) for value in self.dpt_raw_drop],
            on_change=self.dpt_drop_changed,
        )

        self.department_empty_textlabel = ft.Text()

        self.market_dropdown = ft.Dropdown(
            hint_text="Choose a market",
            width=200,
            options=[ft.dropdown.Option(value) for value in self.mkt_raw_drop],
            on_change=self.mkt_drop_changed,
        )

        self.market_empty_textlabel = ft.Text()

        # Combobox and dropdowns for reports page
        self.dpt_rp_drop = consolidate.GatherData().form_combo("department")
        self.dpt_rp_drop_var = None

        self.dpt_rp_dropdown = ft.Dropdown(
            hint_text="Choose a department",
            width=300,
            options=[ft.dropdown.Option(value) for value in self.dpt_rp_drop],
            on_change=self.dpt_rp_drop_changed,
        )

        self.dpt_rp_empty_textlabel = ft.Text()

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
        # Show initial content
        self.show_home

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
                src="assets/comp_logo.jpg",
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
                ft.NavigationDestination(
                    icon=ft.icons.REFRESH_SHARP, label="Refresh App"
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

            self.process_data_frame(df)

    def process_data_frame(self, df):
        print("Appending in")
        file_ops.FilePrep()._append_to_df(df)
        print("Appending done. wait for the confirmation message")

        return self.show_confimation(
            "Upload Successful",
            "The file has been successfully uploaded intop the central file. \nPress anywhere to dismiss this prompt",
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
                            on_click=self.create_file_picker,
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
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Generate report for department"),
                                self.dpt_rp_dropdown,
                                self.dpt_rp_empty_textlabel,
                            ]
                        ),
                        ft.Column(
                            [
                                ft.ElevatedButton(
                                    "Generate QvQ report",
                                    icon="add",
                                    on_click=lambda _: report_builder.BuildReport(
                                        self.dpt_rp_drop_var
                                    ).build_report(),
                                ),
                                # TODO: needs to be added on a new control
                                ft.ElevatedButton(
                                    "Generate QvQ all reports",
                                    icon="add",
                                    on_click=lambda _: report_builder.BuildReport(
                                        self.dpt_rp_drop_var
                                    ).build_report_all(),
                                ),
                            ]
                        ),
                    ]
                ),
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_500,
                border_radius=10,
            ),
        ]

        self.page.update()

    def dpt_drop_changed(self, e):
        self.dpt_dropdown_var = e.control.value
        self.department_empty_textlabel.value = (
            f"Selected Value: {self.dpt_dropdown_var}"
        )

        self.content.controls[1].controls[1].content = self.update_dept_table(
            self.dpt_dropdown_var
        )

        self.page.update()

    def mkt_drop_changed(self, e):
        self.mkt_dropdown_var = e.control.value
        self.market_empty_textlabel.value = f"Selected Value: {self.mkt_dropdown_var}"

        # woould update with the following formula: self.content.controls[index].controls [val].content
        self.content.controls[3].controls[1].content = self.update_mkt_table(
            self.mkt_dropdown_var
        )

        self.page.update()

    def dpt_rp_drop_changed(self, e):
        self.dpt_rp_drop_var = e.control.value
        self.dpt_rp_empty_textlabel.value = f"Selected Value: {self.dpt_rp_drop_var}"

        self.page.update()

    def update_dept_table(self, cval):
        df = file_ops.FilePrep().split_by_snap()[1]

        df_to_convert = kpi_department.EmployeeAnalytics(df, cval).form_df()

        return ft.DataTable(
            columns=consolidate.headers(df_to_convert),
            rows=consolidate.rows(df_to_convert),
        )

    def update_mkt_table(self, cval):
        df = file_ops.FilePrep().split_by_snap()[1]

        df_to_convert = kpi_market.CountryAnalytics(df, cval).form_df()

        return ft.DataTable(
            columns=consolidate.headers(df_to_convert),
            rows=consolidate.rows(df_to_convert),
        )

    def show_home(self, e):
        table1 = self.update_dept_table(self.dpt_dropdown_var)
        table2 = self.update_mkt_table(self.mkt_dropdown_var)

        combo_cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Department section"),
                    self.department_dropdown,
                    self.department_empty_textlabel,
                ]
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_700,
            width=350,
            height=150,
            border_radius=10,
        )

        table_cont = ft.Container(
            content=ft.Row(
                [
                    table1,
                ]
            ),
            bgcolor=ft.colors.GREEN_700,
            margin=10,
            alignment=ft.alignment.center,
            border_radius=10,
            width=800,
            padding=10,
        )

        market_combo_cont = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Market section"),
                    self.market_dropdown,
                    self.market_empty_textlabel,
                ]
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_700,
            width=350,
            height=150,
            border_radius=10,
        )

        market_table_cont = ft.Container(
            content=ft.Row(
                [
                    table2,
                ]
            ),
            bgcolor=ft.colors.GREEN_700,
            margin=10,
            alignment=ft.alignment.center,
            border_radius=10,
            width=800,
            padding=10,
        )

        if self.default_width < self.modified_width:
            self.page.width = self.modified_width

        def toggle_icon_button(e):
            e.control.selected = not e.control.selected
            self.show_confimation("Data Linked", "Data have the same source")
            e.control.update()

        self.content.controls = [
            ft.Text("Welcome to the KPI Reporting App"),  # index 0
            ft.Row([combo_cont, table_cont]),  # index 1
            # TODO: Create an intersection class and link the data between the 2 tables. Not urgent
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.LINK_OFF_OUTLINED,
                        selected_icon=ft.icons.LINK_OUTLINED,
                        icon_color=ft.colors.PINK_600,
                        icon_size=40,
                        tooltip="Link department and market",
                        on_click=toggle_icon_button,
                        selected=False,
                        style=ft.ButtonStyle(
                            color={
                                "selected": ft.colors.GREEN_600,
                                "": ft.colors.RED_600,
                            }
                        ),
                    )
                ]
            ),
            ft.Row([market_combo_cont, market_table_cont]),  # index 3
            #           val 0, val 1
        ]

        def check_dimensions():
            combo_cont_width = combo_cont.width or 0
            combo_cont_margin = combo_cont.margin or 0
            combo_cont_border = combo_cont.border_radius or 0
            table_cont_width = table_cont.width or 0
            table_cont_margin = table_cont.margin or 0
            table_cont_border = table_cont.border_radius or 0

            self.modified_width = (
                combo_cont_width
                + combo_cont_margin * 2
                + combo_cont_border * 2
                + table_cont_width
                + table_cont_margin * 2
                + table_cont_border * 2
                + 171
            )

            if self.default_width < self.modified_width:
                self.page.window_width = self.modified_width
                self.page.update()

        threading.Timer(0.3, check_dimensions).start()
        self.page.update()

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

    def refresh_app(self, e):
        t_open = threading.Thread(target=AppFace(ft.Page))
        t_close = threading.Thread(target=self.page.window_close())

        t_open.start()
        t_close.start()

        self.page.update()

    def check_item_clicked(self, param):
        param.control.checked = not param.control.checked
        self.page.update()

    def change_theme(self, theme_mode: ft.ThemeMode):
        self.page.theme_mode = theme_mode
        self.page.update()
        self.logger.log("info", f"Theme changed to {theme_mode}")

    def on_nav_change(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.show_home(e)
        elif selected_index == 1:
            self.show_report_downloader(e)
        elif selected_index == 2:
            self.show_plot(e)
        elif selected_index == 3:
            self.show_settings(e)
        elif selected_index == 4:
            self.refresh_app(e)
