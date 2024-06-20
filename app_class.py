import flet as ft  # type: ignore
from logs.logger_class import GrabLogs


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

    def show_home(self, e):
        self.content.controls = [ft.Text("Welcome to the KPI Reporting App")]
        self.page.update()

    def show_report_downloader(self, e):
        self.content.controls = [
            ft.Text("This Section is used to check data and download reports")
        ]
        self.page.update()

    def show_plot(self, e):
        self.content.controls = [ft.Text("Plot Section under construction")]
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
