import matplotlib.pyplot as plt
from logics.constants import NUM_STATIONS, NUM_RESERVATION, NUM_TOTAL_CALLS, CELL_DIAMETER, WARM_UP_TIME

from logics.System import System

if __name__ == '__main__':
    x = []
    y = []
    z = []
    simulation_system = System(NUM_STATIONS, NUM_RESERVATION, NUM_TOTAL_CALLS, CELL_DIAMETER, WARM_UP_TIME)

    while simulation_system.is_not_end():
        x.append(simulation_system.clk)
        y.append(simulation_system.get_avg_busy_channels())
        z.append(len(simulation_system.event_list))
        simulation_system.update()

    print("Blocked Calls: " + str(simulation_system.blocked_calls*100/simulation_system.total_calls))
    print("Dropped Calls: " + str(simulation_system.dropped_calls*100/simulation_system.total_calls))
    print(simulation_system.clk)

    fig1 = plt.figure(figsize=(10, 5))
    plt.plot(x, y, color='#0000ff')
    plt.axvline(x=WARM_UP_TIME, color='#ff0000')
    plt.title('Average busy station channels against simulation clock')
    plt.ylabel('Average busy station channels')
    plt.xlabel('Simulation clock/sec')
    fig1.savefig('output/warm_up/' + 'busy_channel.png', dpi=300)
    fig2 = plt.figure(figsize=(10, 5))
    plt.plot(x, z, color='#0000ff')
    plt.axvline(x=WARM_UP_TIME, color='#ff0000')
    plt.title('Number of events in the event list against simulation clock')
    plt.ylabel('Number of events in the event list')
    plt.xlabel('Simulation clock/sec')
    fig2.savefig('output/warm_up/' + 'event_list.png', dpi=300)
    plt.show()
