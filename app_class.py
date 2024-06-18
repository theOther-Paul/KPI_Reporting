import flet as ft  # type: ignore


# The `AppFace` class creates a simple app interface with a sidebar navigation rail and content area
# for home, profile, and settings pages.
class AppFace:
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
                    icon=ft.icons.HOME,
                    selected_icon=ft.icons.HOME,
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PERSON,
                    selected_icon=ft.icons.PERSON,
                    label="Profile",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.on_nav_change,
        )

        return rail

    def show_home(self, e):
        self.content.controls = [ft.Text("This is the home page.")]
        self.page.update()

    def show_profile(self, e):
        self.content.controls = [ft.Text("This is the profile page.")]
        self.page.update()

    def show_settings(self, e):
        self.content.controls = [ft.Text("This is the settings page.")]
        self.page.update()

    def on_nav_change(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.show_home(e)
        elif selected_index == 1:
            self.show_profile(e)
        elif selected_index == 2:
            self.show_settings(e)
