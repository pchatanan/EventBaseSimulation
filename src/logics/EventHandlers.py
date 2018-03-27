from events.CallHandoverEvent import CallHandoverEvent
from events.CallInitEvent import CallInitEvent
from events.CallTerminateEvent import CallTerminateEvent
from logics.DisManager import RanVar


def handle_init_call(call_init_event, system):
    if system.total_calls != system.num_total_calls:
        # Schedule new call_init_event
        new_call_init_event = CallInitEvent(
            system.clk + system.distribution_manager.get_rand_var(RanVar.InterArrTime),
            system.distribution_manager.get_rand_var(RanVar.Velocity),
            system.distribution_manager.get_rand_var(RanVar.BaseStn),
            system.distribution_manager.get_rand_var(RanVar.Position),
            system.distribution_manager.get_rand_var(RanVar.CallDur),
            system.distribution_manager.get_rand_var(RanVar.Direction)
        )
        system.queue_event(new_call_init_event)

    # Check if there is channel available
    available_channel = system.station_list[call_init_event.station].get_available_channel()
    if available_channel > system.num_reservation:
        system.station_list[call_init_event.station].busy_channel_count += 1

        # determine if handover will happen
        stn_heading_to = (call_init_event.station + 1) if call_init_event.direction else (call_init_event.station - 1)
        distance_to_border = (2.0 - call_init_event.position) if call_init_event.direction else call_init_event.position
        time_to_border = (distance_to_border / call_init_event.speed) * 60 * 60
        call_end_before_crossing = call_init_event.duration < time_to_border
        if stn_heading_to < 0 or stn_heading_to > system.num_stations - 1 or call_end_before_crossing:
            # Schedule call termination event
            call_terminate_event = CallTerminateEvent(system.clk + call_init_event.duration,
                                                      call_init_event.station)
            system.queue_event(call_terminate_event)
        else:
            # Schedule call handover event
            handover_event = CallHandoverEvent(system.clk + time_to_border,
                                               call_init_event.speed,
                                               call_init_event.station,
                                               call_init_event.duration - time_to_border,
                                               call_init_event.direction)
            system.queue_event(handover_event)

    elif system.clk > system.warm_up_time:
        system.blocked_calls += 1


def handle_terminate_call(call_terminate_event, system):
    system.station_list[call_terminate_event.station].busy_channel_count -= 1


def handle_handover_call(call_handover_event, system):
    # release channel from previous station
    system.station_list[call_handover_event.station].busy_channel_count -= 1
    # occupy channel of current station
    current_station = (call_handover_event.station + 1) if call_handover_event.direction else (call_handover_event.station - 1)

    available_channel = system.station_list[current_station].get_available_channel()
    if available_channel > 0:
        system.station_list[current_station].busy_channel_count += 1

        # check if call terminate before crossing
        new_station = (current_station + 1) if call_handover_event.direction else (current_station - 1)
        distance_to_border = 2.0
        time_to_border = (distance_to_border / call_handover_event.speed) * 60 * 60
        call_end_before_crossing = call_handover_event.duration < time_to_border
        if new_station < 0 or new_station > system.num_stations - 1 or call_end_before_crossing:
            # Schedule call termination event
            call_terminate_event = CallTerminateEvent(system.clk + call_handover_event.duration,
                                                      current_station)
            system.queue_event(call_terminate_event)
        else:
            # Schedule call handover event
            new_handover_event = CallHandoverEvent(system.clk + time_to_border,
                                                   call_handover_event.speed,
                                                   current_station,
                                                   call_handover_event.duration - time_to_border,
                                                   call_handover_event.direction)
            system.queue_event(new_handover_event)
    elif system.clk > system.warm_up_time:
        system.dropped_calls += 1
