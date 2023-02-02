"""
Calculations:
"""

from __init__ import ureg, Q_
from math import log, e
import numpy as np


def calc_biot(h_value=None, k_value=None, thickness=None):
    L_c = thickness
    biot = h_value * L_c / k_value
    return biot


def stability_analysis(h_value=None, k_value=None, thickness=None, rho=None, cp=None, dx=None):
    biot = h_value * thickness / k_value
    alpha = k_value / (rho * cp)

    # Stability equations for each node
    dt1 = (2 * dx**2 / (alpha * (2 + biot))).to(ureg.seconds)
    dt2 = (dx**2 / (alpha * 2 * (2 + biot))).to(ureg.seconds)
    dt3 = (dx**2 / (alpha * 4 * (1 + biot))).to(ureg.seconds)
    dt4 = (dx**2 / (alpha * 3)).to(ureg.seconds)
    dt5 = (dx**2 / (alpha * 4)).to(ureg.seconds)

    value_list = [dt1, dt2, dt3, dt4, dt5]

    # Return the minimum value
    min_dt = min(value_list)
    return min_dt


def calc_fo(k_value=None, rho=None, cp=None, delta_t=None, delta_x=None):
    alpha = k_value / (rho * cp)
    fo = (alpha * delta_t / (delta_x ** 2)).to('dimensionless')
    return fo


def calc_lumped_capacitance(T_amb=None, T_i=None, h_value=None, rho=None, thickness=None, width=None, cp=None,
                            flux=None, T_final=None, time=None):
    """
    This function finds the time required to reach T_final OR the temperature at the given time value.
    Assumes no energy generation. Surface area is the top surface of the plancha only.
    """
    a = (h_value * width) / (rho * thickness * width * cp)
    b = (flux * width) / (rho * thickness * width * cp)
    if time is None:
        # Solve for time
        t = log((T_final - T_amb - (b / a)) / (T_i - T_amb - (b / a))) * (-1 / a)
        return t
    elif T_final is None:
        # Solve for T_final
        Temp = (T_i - T_amb) * e ** (-a * time) + (b / a) / (T_i - T_amb) * (1 - e ** (-a * time)) + T_amb
        return Temp
    else:
        return Exception("Error in calc_lumped_capacitance function")


def calc_stored_energy_per_time(rho=None, thickness=None, width=None, cp=None, T_i=None, T_final=None, time=None):
    # Calc energy stored at operating temp. Requires input for time to reach operating temp.
    energy_stored_per_length_per_time = rho * width * thickness * cp * (T_final - T_i) / time
    return energy_stored_per_length_per_time


def calc_convection_heat_loss(h_value=None, thickness=None, width=None, T_amb=None, T_plancha=None):
    # Calc heat lost to convection per length at operating temperature.
    # Assumes uniform temperature along top and sides of plancha.
    conv_heat_sides = 2 * h_value * thickness * (T_plancha - T_amb)
    conv_heat_top = h_value * width * (T_plancha - T_amb)
    conv_heat_loss_per_length = conv_heat_top + conv_heat_sides
    return conv_heat_loss_per_length


def calc_steady_state_temp(flux=None, h_value=None, thickness=None, width=None, T_amb=None):
    # Find steady state temperature of the center of the plancha
    T_ss = T_amb + (flux * width) / (h_value * (2 * thickness + width))
    assert T_ss.units == ureg.degK
    return T_ss


def calc_finite_difference(fo=None, biot=None, T_i=None, flux=None, k_value=None, thickness=None,
                           width=None, T_amb=None, dx=None, time=Q_(3100, ureg.seconds), dt=None, T_s=None):
    # Find time to reach T_s at center of plancha surface
    temp_arr_list = []
    new_temp_arr_list = []

    # Testing
    rows = int(thickness.magnitude / dx.magnitude)
    cols = int(width.magnitude / dx.magnitude)
    times = int(time.magnitude / dt.magnitude)
    print(dt)
    print(time)

    for t in range(times):
        # Testing
        print(t * dt)

        # Set initial values
        if t == 0:
            for i in range(rows):
                col = []
                for j in range(cols):
                    temp = T_i
                    col.append(temp)
                temp_arr_list.append(col)
            temp_arr = np.array(temp_arr_list, dtype=object)
            temp_arr_list = []

        # Calculate p+1 values
        for i in range(rows):   # y-dir
            col = []
            for j in range(cols):   # x-dir
                if j == 0 and i == 0:   # BLC
                    temp_next = fo / 2 * (temp_arr[i, j + 1] + temp_arr[i + 1, j] + biot * T_amb) + \
                                    (1 - fo - 0.5 * biot * fo) * temp_arr[i, j] + dx / k_value * fo * flux
                    col.append(temp_next.to(ureg.degK))
                elif j == cols-1 and i == 0:    # BRC
                    temp_next = fo / 2 * (temp_arr[i, j - 1] + temp_arr[i + 1, j] + biot * T_amb) + \
                                    (1 - fo - 0.5 * biot * fo) * temp_arr[i, j] + dx / k_value * fo * flux
                    col.append(temp_next.to(ureg.degK))
                elif 0 < j < cols-1 and i == 0:     # Bottom
                    temp_next = fo / 2 * (temp_arr[i, j + 1] + temp_arr[i, j - 1] + 4 * temp_arr[i + 1, j]) + \
                                        temp_arr[i, j] * (1 - 3 * fo) + dx / k_value * fo * flux
                    col.append(temp_next.to(ureg.degK))
                elif j == 0 and i == rows-1:    # TLC
                    temp_next = 2 * fo * (temp_arr[i, j + 1] + temp_arr[i - 1, j] + 2 * biot * T_amb) + \
                                    (1 - 4 * fo - 4 * biot * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                elif j == cols-1 and i == rows-1:   # TRC
                    temp_next = 2 * fo * (temp_arr[i, j - 1] + temp_arr[i - 1, j] + 2 * biot * T_amb) + \
                                    (1 - 4 * fo - 4 * biot * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                elif 0 < j < cols-1 and i == rows-1:    # Top
                    temp_next = fo * (temp_arr[i - 1, j] + temp_arr[i, j - 1] + temp_arr[i, j + 1] + 2 * biot * T_amb) + \
                                    (1 - 4 * fo - 2 * biot * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                elif j == 0 and 0 < i < rows-1:     # Left
                    temp_next = fo * (2 * temp_arr[i, j + 1] + temp_arr[i + 1, j] + temp_arr[i - 1, j] +
                                           2 * biot * T_amb) + (1 - 4 * fo - 2 * biot * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                elif j == cols-1 and 0 < i < rows-1:   # Right
                    temp_next = fo * (2 * temp_arr[i, j - 1] + temp_arr[i + 1, j] + temp_arr[i - 1, j] +
                                            2 * biot * T_amb) + (1 - 4 * fo - 2 * biot * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                elif 0 < j < cols-1 and 0 < i < rows-1:   # Interior
                    temp_next = fo * (temp_arr[i, j + 1] + temp_arr[i, j - 1] + temp_arr[i + 1, j] +
                                               temp_arr[i - 1, j]) + (1 - 4 * fo) * temp_arr[i, j]
                    col.append(temp_next.to(ureg.degK))
                else:
                    Exception('Error in finite difference function')

            new_temp_arr_list.append(col)

        # Move list p+1 values to numpy array and clear list
        new_temp_arr = np.array(new_temp_arr_list, dtype=object)
        new_temp_arr_list = []

        # Move p+1 values to p array
        for i in range(rows):
            for j in range(cols):
                temp_arr[i, j] = new_temp_arr[i, j]

        # Check if operating temp has been reached
        top_center_temp = (temp_arr[rows-1, int(0.5*(cols-1))]).to(ureg.degK)
        if top_center_temp >= T_s:
            return t * dt

    top_center_temp = (temp_arr[rows-1, int((cols-1)*0.5)]).to(ureg.degK)
    return top_center_temp


if __name__ == "__main__":
    print('Executed')
