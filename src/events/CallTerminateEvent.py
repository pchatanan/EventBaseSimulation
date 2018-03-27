from .BaseEvent import BaseEvent, EventType


class CallTerminateEvent(BaseEvent):
    def __init__(self, time, station):
        BaseEvent.__init__(self, EventType.CALL_TERMINATE, time)
        self.station = station
