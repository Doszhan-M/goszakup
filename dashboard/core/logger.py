config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": " {asctime} - {levelname} - {message}",
            "datefmt": "%H:%M:%S",
            "style": "{",
        },
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(yellow)s%(asctime)-8s%(reset)s - %(log_color)s%(levelname)-1s%(reset)s - %(message)s",
            "datefmt": "%H:%M:%S",
            "log_colors": {
                "DEBUG": "bold_black",
                "INFO": "green",
                "WARNING": "light_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "red,bg_white",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "color",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/info.log",
            "formatter": "color",
            "when": "midnight",
            "backupCount": 7,
        },
        "celery.file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/celery.log",
            "formatter": "color",
            "when": "midnight",
            "backupCount": 7,
        },
        "sql_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],  # "file"],
            "level": "INFO",
            "propagate": True,
        },
        "gunicorn": {
            "handlers": ["console"],  # "file"],
            "level": "INFO",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],  # "celery.file"],
            "level": "INFO",
            "propagate": True,
        },
        # 'django.db.backends': { # закомментировать для выключения вывода sql запросов
        #     'level': 'DEBUG',
        #     'handlers': ["sql_console"],
        #     "propagate": False,
        # },
    },
}
