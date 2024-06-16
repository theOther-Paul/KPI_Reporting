import flet as ft  # type: ignore


class AppFace(ft.Column):
    def __init__(self):
        super().__init__()
        bg_container = ft.Ref[ft.Container]()

        def handle_color_click(e):
            color = e.control.content.value
            print(f"{color}.on_click")
            bg_container.current.content.value = f"{color} background color"
            bg_container.current.bgcolor = color.lower()

        def handle_on_hover(e):
            print(f"{e.control.content.value}.on_hover")

        menubar = ft.MenuBar(
            expand=True,
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("BgColors"),
                    controls=[
                        ft.SubmenuButton(
                            content=ft.Text("B"),
                            leading=ft.Icon(ft.icons.COLORIZE),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Blue"),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.MaterialState.HOVERED: ft.colors.BLUE
                                        }
                                    ),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                )
                            ],
                        ),
                        ft.SubmenuButton(
                            content=ft.Text("G"),
                            leading=ft.Icon(ft.icons.COLORIZE),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Green"),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.MaterialState.HOVERED: ft.colors.GREEN
                                        }
                                    ),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                )
                            ],
                        ),
                        ft.SubmenuButton(
                            content=ft.Text("R"),
                            leading=ft.Icon(ft.icons.COLORIZE),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Red"),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.MaterialState.HOVERED: ft.colors.RED
                                        }
                                    ),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                )
                            ],
                        ),
                    ],
                )
            ],
        )
