import flet as ft  # type: ignore
from app_class import AppFace
from pathlib import Path

def main(page: ft.Page):
    page.title = "KPI Reporting v.01"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # rail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.Image(
            src=f"assets/comp_logo.jpg",
            width=100,
            height=100,
            fit=ft.ImageFit.CONTAIN,
        ),
        group_alignment=-0.9,
        destinations=[
            ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER,
                selected_icon=ft.icons.FAVORITE,
                label="First",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )
    # create application instance
    app = AppFace()

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [ft.Text("Body!")],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

    # add application's root control to the page
    page.add(app)

    # update before launching
    page.update()

ft.app(main)
