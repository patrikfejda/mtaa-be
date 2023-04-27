import signal
from typing import Callable


def timeout(func: Callable, args=(), kwargs={}, timeout_duration: int = 1, default=None):
    """
    Returns the result of a function or None if it takes longer than timeout_duration to execute.
    Works only on UNIX based systems.
    Source: https://stackoverflow.com/a/13821695
    """

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)

    try:
        result = func(*args, **kwargs)
    except TimeoutError:
        result = default
    finally:
        signal.alarm(0)

    return result
