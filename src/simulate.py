import matplotlib.pyplot as plt
import scipy.stats
import numpy as np

from logics.constants import *

from logics.System import System
import math

simulation_loop = SIMULATION_LOOP


def get_probability(data_list, bins, title, limit):

    fig = plt.figure(figsize=(6, 4))
    hist, bin_edges, patches = plt.hist(data_list, bins=bins, color='#5D6D7E', edgecolor='white', linewidth=0.3,
                                        normed=True, histtype='bar')
    mid_values = (bin_edges + np.roll(bin_edges, -1))[:-1] / 2.0

    dist = getattr(scipy.stats, 'norm')

    # fit dist to data
    params = dist.fit(data_list)

    print("Normal distribution params: " + str(params))

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    pdf = dist.pdf(mid_values, loc=loc, scale=scale, *arg)

    bin_edges = np.linspace(min(data_list), max(data_list), bins)
    plt.plot(bin_edges, pdf, label='norm', color='r')
    plt.title(title)

    fig.savefig('output/qos_probability/' + 'qos_' + title + '_reserve_' + str(NUM_RESERVATION) + '.png', dpi=300)

    return dist.cdf(limit, loc=loc, scale=scale)


if __name__ == '__main__':

    sum_blocked_calls = []
    sum_dropped_calls = []
    pass_qos_num = 0

    for i in range(simulation_loop):
        print(simulation_loop - i)
        simulation_system = System(NUM_STATIONS, NUM_RESERVATION, NUM_TOTAL_CALLS, CELL_DIAMETER, WARM_UP_TIME)
        while simulation_system.is_not_end():
            simulation_system.update()

        percent_blocked_calls = simulation_system.blocked_calls * 100 / simulation_system.total_calls
        percent_dropped_calls = simulation_system.dropped_calls * 100 / simulation_system.total_calls

        sum_blocked_calls.append(percent_blocked_calls)
        sum_dropped_calls.append(percent_dropped_calls)

        if percent_blocked_calls < 2.0 and percent_dropped_calls < 1.0:
            pass_qos_num += 1

    blocked_pass_prob = get_probability(sum_blocked_calls, round(math.sqrt(simulation_loop)), 'blocked calls', BLOCKED_CALL)
    dropped_pass_prob = get_probability(sum_dropped_calls, round(math.sqrt(simulation_loop)), 'dropped calls', DROPPED_CALL)

    print("Blocked Calls: " + str(sum(sum_blocked_calls) / simulation_loop) + '%')
    print("Dropped Calls: " + str(sum(sum_dropped_calls) / simulation_loop) + '%')
    print("Pass: " + str(pass_qos_num * 100 / simulation_loop) + '%')

    print("Blocked Calls: " + str(blocked_pass_prob * 100) + '%')
    print("Dropped Calls: " + str(dropped_pass_prob * 100) + '%')
    print("Pass: " + str(blocked_pass_prob * dropped_pass_prob * 100) + '%')

    plt.show()
