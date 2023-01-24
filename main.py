"""
Project 1 - Assumptions (Given):
    - heat is lost out the top and sides of plancha
        through convection
    - Radiation is negligible
    - Assume 2D rectangular operation across the cross-
        section (uniform across the length)

Calculations:
    - Compare the time for the top center of the
        plancha to reach 250 C for each
    - Calculate stored energy at operating temperature
    - Determine heat lost to convection per length at
        operating temperature (assume uniform temp at
        top and sides for this)
    - Find steady-state temp of the center of the plancha
        for each material
    - What should applied flux be reduced to in order to
        achieve constant operating temp?
    - Recalculate time to reach operating temp if convective
        HT coefficient is halved
"""

from __init__ import ureg, Q_
import calc_functions as cf


def main():

    # Given Variables
    width = Q_(45, ureg.cm).to(ureg.meter)
    thickness = Q_(1, ureg.cm).to(ureg.meter)
    heat_flux = Q_(4500, ureg.watts / ureg.meter**2)    # Biomass fire

    T_amb = Q_(27, ureg.degC).to(ureg.degK)
    h_air = Q_(15, ureg.watts / (ureg.meter**2 * ureg.degK))
    T_i = Q_(305, ureg.degK)
    T_s = Q_(250, ureg.degC).to(ureg.degK)     # Operating Temp

    # Material properties (478K) - Ceramic "Fireclay brick"
    rho_fireclay_478 = Q_(2645, ureg.kg / ureg.meters**3)
    cp_fireclay_478 = Q_(960, ureg.joules / (ureg.kg * ureg.degK))
    k_fireclay_478 = Q_(1, ureg.watts / (ureg.meters * ureg.degK))

    # Material properties (300K) - Cast iron "plain carbon steel"
    rho_cast_iron_300 = Q_(7854, ureg.kg / ureg.meters**3)
    cp_cast_iron_300 = Q_(434, ureg.joules / (ureg.kg * ureg.degK))
    k_cast_iron_300 = Q_(60.5, ureg.watts / (ureg.meters * ureg.degK))
    alpha_cast_iron_300 = Q_(17.7 * 10**6, ureg.meters**2 / ureg.seconds)

    # Material properties (300K) - Aluminum
    rho_al_300 = Q_(2702, ureg.kg / ureg.meters**3)
    cp_al_300 = Q_(903, ureg.joules / (ureg.kg * ureg.degK))
    k_al_300 = Q_(237, ureg.watts / (ureg.meters * ureg.degK))
    alpha_al_300 = Q_(97.1 * 10**6, ureg.meters**2 / ureg.seconds)

    """
    Analysis
    """

    # Check Biot number
    biot_al = cf.calc_biot(h_value=h_air, k_value=k_al_300, thickness=thickness, width=width)
    biot_fireclay = cf.calc_biot(h_value=h_air, k_value=k_fireclay_478, thickness=thickness, width=width)
    biot_cast_iron = cf.calc_biot(h_value=h_air, k_value=k_cast_iron_300, thickness=thickness, width=width)

    print("The Biot numbers for each material is as follows... ")
    print("    Aluminum: {}".format(round(biot_al, 3)))
    print("    Ceramic: {}".format(round(biot_fireclay, 3)))
    print("    Cast Iron: {}".format(round(biot_cast_iron, 3)))
    print("...")

    """
    Task 1: Compare the time for the top center of the plancha to reach 250°C for the three materials.
    Even if lumped capacitance does not apply, enter the results and compare to Finite
    Difference, if applicable.
    """

    # METHOD 1: LUMPED CAPACITANCE

    delta_t_lumped_al = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air, rho=rho_al_300,
                                                   thickness=thickness, width=width, cp=cp_al_300, flux=heat_flux,
                                                   T_final=T_s).to(ureg.seconds)
    delta_t_lumped_fireclay = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air, rho=rho_fireclay_478,
                                                         thickness=thickness, width=width, cp=cp_fireclay_478,
                                                         flux=heat_flux, T_final=T_s).to(ureg.seconds)
    delta_t_lumped_cast_iron = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air, rho=rho_cast_iron_300,
                                                          thickness=thickness, width=width, cp=cp_cast_iron_300,
                                                          flux=heat_flux, T_final=T_s).to(ureg.seconds)

    # TODO: Compare with Finite Difference Method

    print("The time to heat to 250 degC for each material is as follows... ")
    print("    Lumped Capacitance method, Aluminum: {}".format(round(delta_t_lumped_al, 2)))
    print("    Lumped Capacitance method, Ceramic: {}".format(round(delta_t_lumped_fireclay, 2)))
    print("    Lumped Capacitance method, Cast Iron: {}".format(round(delta_t_lumped_cast_iron, 2)))
    print("...")

    """
    Task 2: Determine the amount of energy that has been stored in the plancha when it reaches the 
    operating temperature of 250°C
    """

    # METHOD 1: LUMPED CAPACITANCE

    energy_stored_lumped_al = cf.calc_stored_energy(rho=rho_al_300, thickness=thickness, width=width, cp=cp_al_300, T_i=T_i,
                                             T_final=T_s, time=delta_t_lumped_al).to(ureg.watts / ureg.meter)
    energy_stored_lumped_ceramic = cf.calc_stored_energy(rho=rho_fireclay_478, thickness=thickness, width=width,
                                                         cp=cp_fireclay_478, T_i=T_i, T_final=T_s,
                                                         time=delta_t_lumped_fireclay).to(ureg.watts / ureg.meter)
    energy_stored_lumped_cast_iron = cf.calc_stored_energy(rho=rho_cast_iron_300, thickness=thickness, width=width,
                                                           cp=cp_cast_iron_300, T_i=T_i, T_final=T_s,
                                                           time=delta_t_lumped_cast_iron).to(ureg.watts / ureg.meter)

    # TODO: Compare with Finite Difference Method

    print("The energy stored in the plancha when it reaches 250 degC for each material is as follows... ")
    print("    Lumped Capacitance method, Aluminum: {}".format(round(energy_stored_lumped_al, 2)))
    print("    Lumped Capacitance method, Ceramic: {}".format(round(energy_stored_lumped_ceramic, 2)))
    print("    Lumped Capacitance method, Cast Iron: {}".format(round(energy_stored_lumped_cast_iron, 2)))
    print("...")

    """
    Task 3: Determine the heat lost to convection per unit length of the plancha when it has reached 
    operating temperature. You may assume uniform temperature on the top and sides of the 
    plancha for this. 
    """

    # TODO: Tasks 3-6


if __name__ == "__main__":
    main()
