from enum import Enum


class EventType(Enum):
    CALL_INIT = 1
    CALL_TERMINATE = 2
    CALL_HANDOVER = 3


class BaseEvent:
    # station properties
    event_type = None
    time = None

    def __init__(self, event_type, time):
        self.event_type = event_type
        self.time = time
