"""
Plots:
• Generate a plot of top center surface temperature versus time during the heating process
for these three materials using both the lumped capacitance and finite difference methods.
• (550 only) Show a 2D plot of the temperature profile across the full plancha at one-half of
the time to heat up for the material that is slowest to come to operating temperature.
"""

from __init__ import ureg, Q_
import matplotlib.pyplot as plt
import numpy as np


def plot_top_center_temp_vs_time(time_array=[Q_(1, ureg.seconds), Q_(2, ureg.seconds), Q_(3, ureg.seconds)],
                                 temp_array=[Q_(4, ureg.degK), Q_(5, ureg.degK), Q_(6, ureg.degK)]):
    # Convert to base units before creating numpy array for plotting
    x = np.array([time.magnitude for time in time_array])
    y = np.array([temp.magnitude for temp in temp_array])

    # Set up plots
    plt.plot(x, y)
    plt.title('Plancha surface temp over time')
    plt.ylabel('Temp (Kelvin)')
    plt.xlabel('Time (seconds)')

    # plot
    plt.show()


def plot_temp_profile_at_half_time(temp_profile=None):
    # Convert to base units before creating numpy array for plotting
    data = temp_profile.magnitude
    coord = np.arange(data.shape)
    # also try
    # coord = np.indices(data.shape)

    # Set up plots
    # ax1 = plt.subplot()
    # l1 = ax1.plot(coord)
    # ax2 = ax1.twinx()
    # l2 = ax2.plot(data)

    plt.plot(coord, data)

    plt.title('Temperature profile at half time')
    plt.ylabel('Thickness (mm)')
    plt.xlabel('Width (cm)')

    # plot
    plt.show()


if __name__ == "__main__":
    array_values = np.array([
        [4, 5, 6],
        [7, 8, 9]
    ])
    array = array_values * ureg.degK
    plot_temp_profile_at_half_time(temp_profile=array)
