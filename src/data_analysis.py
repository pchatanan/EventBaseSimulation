import matplotlib.pyplot as plt

from logics.DisManager import DistManager
from logics.constants import NUM_STATIONS, CELL_DIAMETER
from utils import IOManager

if __name__ == '__main__':
    raw_data_dict = IOManager.get_raw_data('../raw/PCS_TEST_DETERMINSTIC_1718S2.xls')
    arr_time_list = raw_data_dict['Arrival time (sec)']
    base_stn_list = raw_data_dict['Base station (sec)']
    call_dur_list = raw_data_dict['Call duration (sec)']
    velocity_list = raw_data_dict['velocity (km/h)']
    inter_arr_time_list = IOManager.get_inter_arr_time(arr_time_list)

    distribution_manager = DistManager(NUM_STATIONS, CELL_DIAMETER)
    distribution_manager.show_dis(base_stn_list, 'Base Station', bins=20)
    distribution_manager.show_dis(inter_arr_time_list, 'Inter Arrival Time', bins=100)
    distribution_manager.show_dis(call_dur_list, 'Call Duration', bins=100)
    distribution_manager.show_dis(velocity_list, 'Car Velocity', bins=100)

    plt.show()

