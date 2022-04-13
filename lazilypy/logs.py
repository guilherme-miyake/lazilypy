import inspect
import logging


def get_logger(name="Lazy Logger"):
    logger = logging.Logger(name, level=30)
    __log_formatter = logging.Formatter(
        "%(levelname)-8s %(asctime)s: %(message)s", datefmt="%Y-%m-%d:%H:%M:%S"
    )
    __log_channel = logging.StreamHandler()
    __log_channel.setFormatter(__log_formatter)
    logger.addHandler(__log_channel)
    return logger


def location_info():
    frame = inspect.currentframe()
    while True:
        previous_frame = frame.f_back
        no_previous_frame = previous_frame is None
        no_globals = not hasattr(previous_frame, "f_globals")
        no_file_context = no_globals or "__file__" not in previous_frame.f_globals
        is_import_frame = (
            no_file_context or "importlib" in previous_frame.f_globals["__file__"]
        )
        if no_previous_frame or no_file_context or is_import_frame:
            break
        frame = frame.f_back

    return f"File \"{frame.f_globals['__file__']}\", line {frame.f_lineno}"


logger = get_logger()
