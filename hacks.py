from logging import Logger
from typing import Callable


def noexcept(log: Logger):
    """
    Grab all uncaught exceptions and log them with the logger
    of the module implementing the decorated function.
    :param log: logger of module using this.
    :return: False
    """
    def noexcept_decorator(f: Callable):
        def noexcept_inner(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return f(*args, **kwargs)
            except:
                log.exception("An unexpected error occurred.")
                return False
        return noexcept_inner
    return noexcept_decorator
