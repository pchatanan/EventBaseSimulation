import random

import matplotlib.pyplot as plt
import scipy
import scipy.stats
from enum import Enum
import numpy as np
from scipy.stats import norm
from scipy.stats import expon


class RanVar(Enum):
    InterArrTime = 1
    BaseStn = 2
    CallDur = 3
    Velocity = 4
    Direction = 5
    Position = 6


class DistManager:

    def __init__(self, num_stations, cell_diameter):
        self.num_stations = num_stations
        self.cell_diameter = cell_diameter

    @staticmethod
    def show_dis(data_list, title, bins=200):
        data_list = np.array(data_list)

        # Best holders
        best_distribution = 'norm'
        best_params = (0.0, 1.0)
        best_mse = np.inf

        fig = plt.figure(figsize=(6, 4))
        hist, bin_edges, patches = plt.hist(data_list, bins=bins, color='#5D6D7E', edgecolor='white', linewidth=0.3, normed=True, histtype='bar')
        mid_values = (bin_edges + np.roll(bin_edges, -1))[:-1] / 2.0

        dist_names = ['norm', 'expon', 'uniform']
        colors = ['#ff0000', '#0000ff', '#00ff00']

        for dist_name, color in zip(dist_names, colors):
            dist = getattr(scipy.stats, dist_name)

            # fit dist to data
            params = dist.fit(data_list)

            # Separate parts of parameters
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]

            # Calculate fitted PDF and error with fit in distribution
            pdf = dist.pdf(mid_values, loc=loc, scale=scale, *arg)
            mse = np.sum(np.power(hist - pdf, 2.0))/len(hist)

            if best_mse > mse > 0:
                best_distribution = dist_name
                best_params = params
                best_mse = mse

            bin_edges = np.linspace(min(data_list), max(data_list), bins)
            plt.plot(bin_edges, pdf, label=dist_name, color=color)
            plt.xlim(int(min(data_list)), int(max(data_list) + 0.5))
            plt.ylim(0, max(hist))

        print(title)
        print(best_distribution)
        print(best_params)
        print(best_mse)

        plt.legend(loc='upper right')
        plt.title(title)

        fig.savefig('output/' + title + '.png', dpi=300)

    def get_rand_var(self, ran_var):
        if ran_var == RanVar.InterArrTime:
            return expon.rvs(loc=2.5087585736028974e-05, scale=1.3697967253638823, size=1)[0]
        elif ran_var == RanVar.BaseStn:
            return random.randint(0, self.num_stations - 1)
        elif ran_var == RanVar.Velocity:
            return norm.rvs(loc=120.07209801685764, scale=9.018606933727643, size=1)[0]
        elif ran_var == RanVar.CallDur:
            return expon.rvs(loc=10.003951603232615, scale=99.8317818241303, size=1)[0]
        elif ran_var == RanVar.Direction:
            return random.randint(0, 1)
        elif ran_var == RanVar.Position:
            return random.uniform(0, self.cell_diameter)
