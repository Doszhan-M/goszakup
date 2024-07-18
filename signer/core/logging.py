import logging
from sys import stderr, stdout
from colorlog import ColoredFormatter


class CustomLogger:

    color_formatter = ColoredFormatter(
        "%(yellow)s%(asctime)-8s%(reset)s - %(log_color)s%(levelname)-1s%(reset)s - %(cyan)s%(message)s (%(black)s%(filename)s:%(lineno)d)",
        datefmt="%d-%m-%Y %H:%M:%S",
        log_colors={
            "DEBUG": "white",
            "INFO": "green",
            "WARNING": "light_yellow",
            "ERROR": "bold_red",
            "CRITICAL": "red,bg_white",
        },
    )

    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s -%(message)s (%(filename)s:%(lineno)d)",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    @classmethod
    def _color_stream_handler(cls):
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(cls.color_formatter)
        return stream_handler

    @classmethod
    def setup(cls):

        handlers = [cls._color_stream_handler()]
        logging.basicConfig(handlers=handlers, level=logging.INFO)
        logger = logging.getLogger("grpc")
        logger.handlers = handlers
        logger.propagate = False
        return logger
