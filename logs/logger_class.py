import logging
import os
import random


class GrabLogs:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(GrabLogs, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def configure_logger(self, fname) -> None:
        if self.__initialized:
            return
        self.__initialized = True

        logging.basicConfig(
            filename=f"{os.getcwd()}\\logs\\{fname}",
            level=logging.DEBUG,
            format="%a(asctime)s %(message)s",
            filemode="a",
        )

    def form_log(self, message, level):
        logging.getLogger("matplotlib.font_manager").disabled = True
        if 11 <= level <= 20:
            logging.info(message)
        elif 20 < level <= 30:
            logging.warning(message)
        elif 30 < level <= 40:
            logging.error(message)
        elif 40 < level <= 50:
            logging.critical(message)
        elif 1 <= level <= 10:
            logging.debug(message)

    def clear_logs(self):
        with open(self.log_file, "w"):
            pass

    @staticmethod
    def get_level(keyword: str = "Info"):
        if keyword.lower() in "Information".lower():
            return random.randint(11, 20)
        elif keyword.lower() in "Warning".lower():
            return random.randint(21, 30)
        elif keyword.lower() in "Error".lower():
            return random.randint(31, 40)
        elif keyword.lower() in "Critical".lower():
            return random.randint(41, 50)
        elif keyword.lower() in "Debug".lower():
            return random.randint(1, 10)
