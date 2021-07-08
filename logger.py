from functools import wraps
import inspect
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # лучше иметь больше логов, чем их нехватку
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(log_file))
    logger.propagate = False
    return logger


def log(file):
    def decorator(func):
        @wraps(func)
        def callf(*args, **kwargs):
            my_logger = get_logger("my", file)
            my_logger.debug(f"Функция {func.__name__} вызвана из функции {inspect.stack()[1][3]}")
            r = func(*args, **kwargs)
            return r
        return callf
    return decorator


if __name__ == '__main__':
    pass
