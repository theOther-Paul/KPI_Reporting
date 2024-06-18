import logging


class Logger:
    def __init__(self, filename):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format_str)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(format_str)
        self.logger.addHandler(file_handler)
