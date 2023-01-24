"""
Calculations:
"""

from math import log, e


def calc_biot(h_value=None, k_value=None, thickness=None, width=None):
    L_c = thickness
    biot = h_value * L_c / k_value
    return biot


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
        t = log((T_final - T_amb - (b / a))/(T_i - T_amb - (b / a))) * (-1 / a)
        return t
    elif T_final is None:
        # Solve for T_final
        Temp = (T_i - T_amb) * e**(-a * time) + (b / a) / (T_i - T_amb) * (1 - e**(-a * time)) + T_amb
        return Temp
    else:
        return Exception("Error in calc_lumped_capacitance function")


def calc_stored_energy(rho=None, thickness=None, width=None, cp=None, T_i=None, T_final=None, time=None):
    # Calc energy stored at operating temp. Requires input for time to reach operating temp.
    energy_stored_per_length = rho * width * thickness * cp * (T_final - T_i) / time
    return energy_stored_per_length


def calc_convection_heat_loss():
    # Calc heat lost to convection per length at operating temperature.
    # Assumes uniform temperature along top and sides of plancha.
    return None


def calc_steady_state_temp():
    # Find steady state temperature of the center of the plancha
    return None


def calc_flux_for_const_temp():
    # Find the flux needed to reach constant operating temp
    return None



