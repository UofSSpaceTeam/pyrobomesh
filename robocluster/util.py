"""Utility functions for robocluster."""

import re
import socket
import ipaddress
from functools import wraps
from inspect import iscoroutinefunction

def ip_info(addr):
    """Verify and detecet ip address family."""
    addr = ipaddress.ip_address(addr)
    if isinstance(addr, ipaddress.IPv6Address):
        return socket.AF_INET6, addr
    else:
        return socket.AF_INET, addr

def as_coroutine(func):
    """
    Convert a function to a coroutine that can be awaited.

    Notes:
    If the function is already a coroutine, it is returned directly.

    """
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if iscoroutinefunction(func):
        return func
    return _wrapper


def duration_to_seconds(duration):
    """
    Convert duration as a string to seconds if needed.

    Args:
        duration (str, float): time in seconds or as text.

    Returns:
        int: seconds in duration, or -1 if duration is invalid.

    Supported units:
        - 'm', 'minute', 'minutes': 60 seconds
        - 's', 'second', 'seconds': 1 seconds
        - 'ms', 'millisecond', 'milliseconds': 0.001 seconds

    """
    if isinstance(duration, (float, int)):
        return duration

    value = -1.0
    units = {
        'm': 60, 'minute': 60, 'minutes': 60,
        's': 1, 'second': 1, 'seconds': 1,
        'ms': 0.001, 'millisecond': 0.001, 'milliseconds': 0.001,
    }

    match = re.match(r'^(\d+)\s*(\w+)$', duration)
    if match:
        duration, unit = match.groups()
        try:
            value = float(duration) * units[unit]
        except KeyError:
            pass

    return value

DEBUG = False

def debug(msg):
    """
    Print msg if DEBUG is True. Usefull for debugging what
    the Robocluster internals are doing. To enable debug messages
    include the following in your program that uses devices::

        import robocluster.util; robocluster.util.DEBUG = True
    """
    if DEBUG:
        print(msg)
