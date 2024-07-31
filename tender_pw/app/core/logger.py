import logging
from sys import stderr, stdout
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:

    color_formatter = ColoredFormatter(
        "%(asctime)s - %(log_color)s%(levelname)-1s%(reset)s - %(cyan)s%(message)s (%(black)s%(filename)s:%(lineno)d)",
        datefmt="%Y-%m-%d %H:%M:%S",
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
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    business_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s -%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    @classmethod
    def _color_stream_handler(cls):
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(cls.color_formatter)
        return stream_handler

    @classmethod
    def _common_file_handler(cls):
        file_handler = TimedRotatingFileHandler(
            filename="app/logs/common.log",
            when="MIDNIGHT",
            backupCount=2,
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(cls.simple_formatter)
        return file_handler

    @classmethod
    def _error_file_handler(cls):
        file_handler = TimedRotatingFileHandler(
            filename="app/logs/error.log",
            when="MIDNIGHT",
            backupCount=2,
        )
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(cls.simple_formatter)
        return file_handler

    @classmethod
    def _business_file_handler(cls):
        file_handler = TimedRotatingFileHandler(
            filename="app/logs/business.log",
            when="MIDNIGHT",
            backupCount=30,
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(cls.business_formatter)
        return file_handler
    
    def set_logger(self):
        """Переопределить логгеры uvicorn и fastapi."""

        handlers = [
            self._color_stream_handler(),
            self._common_file_handler(),
            self._error_file_handler(),
        ]
        logging.basicConfig(handlers=handlers, level=logging.INFO)
        for _log in [
            "fastapi",
            "uvicorn.access",
            "uvicorn",
            "uvicorn.error",
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = handlers
            _logger.propagate = False

        business_logger = logging.getLogger("business")
        business_handler = self._business_file_handler()
        business_logger.setLevel(logging.INFO)
        business_logger.addHandler(business_handler)
        business_logger.propagate = False 
        
        return logging.getLogger("fastapi")
