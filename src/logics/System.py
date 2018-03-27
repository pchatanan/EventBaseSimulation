from logics.DisManager import DistManager, RanVar

from entities.Station import Station
from events.BaseEvent import EventType
from events.CallInitEvent import CallInitEvent
from logics import EventHandlers


class System:
    def __init__(self, num_stations, num_reservation, num_total_calls, cell_diameter, warm_up_time):

        self.num_reservation = num_reservation
        self.num_stations = num_stations
        self.num_total_calls = num_total_calls
        self.cell_diameter = cell_diameter
        self.warm_up_time = warm_up_time

        self.distribution_manager = DistManager(num_stations, cell_diameter)

        # stats count
        self.blocked_calls = 0
        self.dropped_calls = 0
        self.total_calls = 0

        # initialise simulation clock to 0
        self.clk = 0
        # initialise 20 stations
        self.station_list = [Station() for i in range(self.num_stations)]
        # empty event list
        self.event_list = []
        # create first event
        call_init_event = CallInitEvent(
            0.0,
            self.distribution_manager.get_rand_var(RanVar.Velocity),
            self.distribution_manager.get_rand_var(RanVar.BaseStn),
            self.distribution_manager.get_rand_var(RanVar.Position),
            self.distribution_manager.get_rand_var(RanVar.CallDur),
            self.distribution_manager.get_rand_var(RanVar.Direction),
        )
        self.queue_event(call_init_event)

    def queue_event(self, event):
        # increment total calls
        if self.clk > self.warm_up_time and event.event_type == EventType.CALL_INIT:
            self.total_calls += 1

        # perform binary insertion
        lower = 0
        upper = len(self.event_list)
        while lower < upper:  # use < instead of <=
            mid = (lower + upper) // 2
            mid_time = self.event_list[mid].time
            if event.time == mid_time:
                self.event_list.insert(mid, event)
                return
            elif event.time > mid_time:
                if lower == mid:
                    self.event_list.insert(upper, event)
                    return
                lower = mid
            elif event.time < mid_time:
                if upper == mid:
                    self.event_list.insert(lower, event)
                    return
                upper = mid
        self.event_list.insert(lower, event)

    def is_not_end(self):
        return self.total_calls != self.num_total_calls and len(self.event_list) != 0

    def update(self):
        event = self.event_list.pop(0)
        # update system time
        self.clk = event.time
        if event.event_type == EventType.CALL_INIT:
            EventHandlers.handle_init_call(event, self)
        elif event.event_type == EventType.CALL_TERMINATE:
            EventHandlers.handle_terminate_call(event, self)
        elif event.event_type == EventType.CALL_HANDOVER:
            EventHandlers.handle_handover_call(event, self)

    def get_avg_busy_channels(self):
        total_busy_channels = 0
        for station in self.station_list:
            total_busy_channels += station.busy_channel_count
        return total_busy_channels / self.num_stations
