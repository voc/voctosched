from logging import Logger, getLogger
from typing import Callable


def noexcept(log: Logger = getLogger(__name__)):
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
            except Exception:
                log.exception("An unexpected error occurred.")
                return False
        return noexcept_inner

    if not isinstance(log, Logger) and callable(log):
        # probably was called without arguments
        actual_log = getLogger(__name__)
        actual_log.warning("\033[1;33mSome monkey used the noexcept decorator without arguments, "
                           "which should not have happened. Go bug the devs about it.\033[1;0m")
        return noexcept_decorator(log)
    return noexcept_decorator
