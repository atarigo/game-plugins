from collections import deque
from enum import Enum
from functools import wraps
from typing import Any, Callable

import structlog

logger = structlog.getLogger(__name__)


def debug(func):
    def readable(value):
        if isinstance(value, Enum):
            return str(value)
        elif isinstance(value, Callable):
            return value.__qualname__
        else:
            return value

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.debug(
            "[Event]",
            action=func.__name__,
            args=[readable(k) for k in args],
            kwargs=kwargs,
        )
        return func(self, *args, **kwargs)

    return wrapper


class EventManager:
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = {}
        self.queue: deque = deque()

    @debug
    def subscribe(self, event_type: str, callback: Callable):
        self.listeners.setdefault(event_type, []).append(callback)

    @debug
    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    @debug
    def emit(self, event_type: str, data: Any = None):
        self.queue.append((event_type, data))

    def process_events(self):
        while self.queue:
            event_type, data = self.queue.popleft()
            logger.debug("[Event]", action="process", event_type=event_type, data=data)
            if event_type in self.listeners:
                for callback in self.listeners[event_type]:
                    callback(data)

    @debug
    def clear(self):
        self.queue.clear()
