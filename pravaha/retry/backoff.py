"""
This file contains several backoff function which returns time.
Closures.
"""
from typing import Optional

def fixed_delay(seconds: float):
    def _backoff(attempt: int):
        return seconds
    return _backoff

def exponential_backoff(base: float = 1.0, factor: int = 2, max_delay: Optional[float] = None):
    def _backoff(attempt: int):
        delay = base * (factor ** (attempt - 1))
        if max_delay:
            delay = min(delay, max_delay)
        return delay
    return _backoff

def no_delay():
    return lambda attempt: 0