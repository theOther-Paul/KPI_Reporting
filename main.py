import flet as ft  # type: ignore
from app_class import AppFace


def main(page: ft.Page):
    page.title = "KPI Reporting v.01"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    app = AppFace()


    # add application's root control to the page
    page.add(app)



ft.app(main)
