from .BaseEvent import BaseEvent, EventType


class CallHandoverEvent(BaseEvent):
    def __init__(self, time, speed, station, duration, direction):
        BaseEvent.__init__(self, EventType.CALL_HANDOVER, time)
        self.speed = speed
        self.station = station
        self.duration = duration
        self.direction = direction
