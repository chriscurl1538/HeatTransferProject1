"""
Plots
"""

from __init__ import ureg, Q_
import matplotlib.pyplot as plt
import numpy as np


# Not currently used
def plot_top_center_temp_vs_time(time_array=None, temp_array=None):
    """
    Generate a plot of top center surface temperature versus time during the heating process
    for these three materials using both the lumped capacitance and finite difference methods.
    """
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


# Not currently used
def plot_temp_profile_at_half_time(temp_profile=None):
    """
    Show a 2D plot of the temperature profile across the full plancha at one-half of
    the time to heat up for the material that is slowest to come to operating temperature.
    """
    # Convert to base units before creating numpy array for plotting
    data = temp_profile.magnitude
    coord = np.arange(data.shape)

    # Set up plots
    plt.plot(coord, data)

    plt.title('Temperature profile at half time')
    plt.ylabel('Thickness (mm)')
    plt.xlabel('Width (cm)')

    # plot
    plt.show()
