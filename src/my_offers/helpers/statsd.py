from functools import wraps
from typing import Any, Callable, TypeVar

from cian_core.statsd import statsd


Func = TypeVar('Func', bound=Callable[..., Any])


def async_statsd_timer(stat: str, rate: int = 1) -> Callable[[Func], Func]:
    def decorator(f: Func) -> Func:
        @wraps(f)
        async def wrapper(*args, **kwargs):
            with statsd.timer(stat=stat, rate=rate):
                return await f(*args, **kwargs)
        return wrapper
    return decorator
