import flet as ft  # type: ignore
from app_class import AppFace
from logs.logger_class import GrabLogs


def main(page: ft.Page):
    AppFace(page)


if __name__ == "__main__":
    logger = GrabLogs().configure_logger("main.log")
    try:
        ft.app(target=main)
        logger.form_log("Application started successfully!", logger.get_level("info"))

    except Exception as e:
        logger.form_log(
            f"Application failed to start because of exception: {e}",
            logger.get_level("crit"),
        )
