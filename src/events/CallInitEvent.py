from .BaseEvent import BaseEvent, EventType


class CallInitEvent(BaseEvent):
    def __init__(self, time, speed, station, position, duration, direction):
        BaseEvent.__init__(self, EventType.CALL_INIT, time)
        self.speed = speed
        self.station = station
        self.position = position
        self.duration = duration
        self.direction = direction
