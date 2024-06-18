import flet as ft  # type: ignore
from app_class import AppFace
from logs import logger_class


def main(page: ft.Page):
    AppFace(page)


if __name__ == "__main__":
    logger = logger_class.Logger("logs/main.log")

    try:
        ft.app(target=main)
        logger.logger.info("Application started succesfully")

    except Exception as e:
        logger.logger.critical(f"App failed to start because of {e}", exc_info=True)
        logger.logger.debug(e, exc_info=True)
