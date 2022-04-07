import inspect
import logging


def get_logger(name='Lazy'):
    logger = logging.Logger(name, level=30)
    __log_formatter = logging.Formatter('%(levelname)-8s %(asctime)s: %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
    __log_channel = logging.StreamHandler()
    __log_channel.setFormatter(__log_formatter)
    logger.addHandler(__log_channel)
    return logger


def location_info():
    frame = inspect.currentframe()
    while True:
        if frame.f_back is None or 'importlib' in frame.f_back.f_globals['__file__']:
            break
        frame = frame.f_back
    return f"File \"{frame.f_globals['__file__']}\", line {frame.f_lineno}"
