"""
Project 1 - Assumptions (Given):
    - heat is lost out the top and sides of plancha
        through convection
    - Radiation is negligible
    - Assume 2D rectangular operation across the cross-
        section (uniform across the length)
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

    # Material properties (300K) - Aluminum
    rho_al_300 = Q_(2702, ureg.kg / ureg.meters**3)
    cp_al_300 = Q_(903, ureg.joules / (ureg.kg * ureg.degK))
    k_al_300 = Q_(237, ureg.watts / (ureg.meters * ureg.degK))

    print("The material properties for Aluminum are... ")
    print("    Conductivity: {}".format(round(k_al_300, 2)))
    print("    Density: {}".format(round(rho_al_300, 2)))
    print("    Specific Heat: {}".format(round(cp_al_300, 2)))
    print("...")

    print("The material properties for Cast Iron are... ")
    print("    Conductivity: {}".format(round(k_cast_iron_300, 2)))
    print("    Density: {}".format(round(rho_cast_iron_300, 2)))
    print("    Specific Heat: {}".format(round(cp_cast_iron_300, 2)))
    print("...")

    print("The material properties for Ceramic are... ")
    print("    Conductivity: {}".format(round(k_fireclay_478, 2)))
    print("    Density: {}".format(round(rho_fireclay_478, 2)))
    print("    Specific Heat: {}".format(round(cp_fireclay_478, 2)))
    print("...")

    """
    Analysis
    """

    # Selected delta x value
    dx = thickness / 3

    # Check Biot number
    biot_al = cf.calc_biot(h_value=h_air, k_value=k_al_300, thickness=thickness)
    biot_fireclay = cf.calc_biot(h_value=h_air, k_value=k_fireclay_478, thickness=thickness)
    biot_cast_iron = cf.calc_biot(h_value=h_air, k_value=k_cast_iron_300, thickness=thickness)

    print("The Biot numbers for each material is as follows... ")
    print("    Aluminum: {}".format(round(biot_al, 3)))
    print("    Cast Iron: {}".format(round(biot_cast_iron, 3)))
    print("    Ceramic: {}".format(round(biot_fireclay, 3)))
    print("...")

    # Calc Fourier number
    dt_al = cf.stability_analysis(h_value=h_air, k_value=k_al_300, thickness=thickness, rho=rho_al_300, cp=cp_al_300,
                                  dx=dx)
    dt_fireclay = cf.stability_analysis(h_value=h_air, k_value=k_fireclay_478, thickness=thickness,
                                        rho=rho_fireclay_478, cp=cp_fireclay_478, dx=dx)
    dt_cast_iron = cf.stability_analysis(h_value=h_air, k_value=k_cast_iron_300, thickness=thickness,
                                         rho=rho_cast_iron_300, cp=cp_cast_iron_300, dx=dx)

    fo_al = cf.calc_fo(k_value=k_al_300, rho=rho_al_300, cp=cp_al_300, delta_t=dt_al, delta_x=dx)
    fo_fireclay = cf.calc_fo(k_value=k_fireclay_478, rho=rho_fireclay_478, cp=cp_fireclay_478, delta_t=dt_fireclay,
                             delta_x=dx)
    fo_cast_iron = cf.calc_fo(k_value=k_cast_iron_300, rho=rho_cast_iron_300, cp=cp_cast_iron_300,
                              delta_t=dt_cast_iron, delta_x=dx)

    print("The Fourier numbers for each material is as follows... ")
    print("    Aluminum: {}".format(round(fo_al, 3)))
    print("    Cast Iron: {}".format(round(fo_cast_iron, 3)))
    print("    Ceramic: {}".format(round(fo_fireclay, 3)))
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

    # # METHOD 2: FINITE DIFFERENCE (UNFINISHED)
    #
    # delta_t_finite_diff_al = cf.calc_finite_difference(fo=fo_al, biot=biot_al, T_i=T_i, flux=heat_flux,
    #                                                    k_value=k_al_300, thickness=thickness, width=width, T_amb=T_amb,
    #                                                    dx=dx, dt=dt_al, T_s=T_s)
    # delta_t_finite_diff_fireclay = cf.calc_finite_difference(fo=fo_fireclay, biot=biot_fireclay, T_i=T_i,
    #                                                          flux=heat_flux, k_value=k_fireclay_478,
    #                                                          thickness=thickness, width=width, T_amb=T_amb, dx=dx,
    #                                                          dt=dt_fireclay, T_s=T_s)
    # delta_t_finite_diff_cast_iron = cf.calc_finite_difference(fo=fo_cast_iron, biot=biot_cast_iron, T_i=T_i,
    #                                                           flux=heat_flux, k_value=k_cast_iron_300,
    #                                                           thickness=thickness, width=width, T_amb=T_amb, dx=dx,
    #                                                           dt=dt_cast_iron, T_s=T_s)

    print("The time to heat to 250 degC for each material is as follows... ")
    print("    Lumped Capacitance method, Aluminum: {}".format(round(delta_t_lumped_al, 2)))
    print("    Lumped Capacitance method, Cast Iron: {}".format(round(delta_t_lumped_cast_iron, 2)))
    print("    Lumped Capacitance method, Ceramic: {}".format(round(delta_t_lumped_fireclay, 2)))
    # print("    Finite Difference method, Aluminum: {}".format(round(delta_t_finite_diff_al, 2)))
    # print("    Finite Difference method, Cast Iron: {}".format(round(delta_t_finite_diff_cast_iron, 2)))
    # print("    Finite Difference method, Ceramic: {}".format(round(delta_t_finite_diff_fireclay, 2)))
    print("...")

    """
    Task 2: Determine the amount of energy that has been stored in the plancha when it reaches the 
    operating temperature of 250°C
    """

    # METHOD 1: LUMPED CAPACITANCE

    energy_stored_lumped_al_per_time = cf.calc_stored_energy_per_time(rho=rho_al_300, thickness=thickness, width=width,
                                                                      cp=cp_al_300, T_i=T_i, T_final=T_s,
                                                                      time=delta_t_lumped_al)
    energy_stored_lumped_al = (energy_stored_lumped_al_per_time * delta_t_lumped_al).to(ureg.kjoules / ureg.meters)

    energy_stored_lumped_ceramic_per_time = cf.calc_stored_energy_per_time(rho=rho_fireclay_478, thickness=thickness,
                                                                           width=width, cp=cp_fireclay_478, T_i=T_i,
                                                                           T_final=T_s, time=delta_t_lumped_fireclay)
    energy_stored_lumped_ceramic = (energy_stored_lumped_ceramic_per_time * delta_t_lumped_fireclay).to(ureg.kjoules /
                                                                                                        ureg.meters)

    energy_stored_lumped_cast_iron_per_time = cf.calc_stored_energy_per_time(rho=rho_cast_iron_300, thickness=thickness,
                                                                             width=width, cp=cp_cast_iron_300, T_i=T_i,
                                                                             T_final=T_s, time=delta_t_lumped_cast_iron).to(ureg.watts / ureg.meter)
    energy_stored_lumped_cast_iron = (energy_stored_lumped_cast_iron_per_time *
                                      delta_t_lumped_cast_iron).to(ureg.kjoules / ureg.meters)

    # # METHOD 2: FINITE DIFFERENCE
    #
    # energy_stored_finite_diff_al_per_time = cf.calc_stored_energy_per_time(rho=rho_al_300, thickness=thickness,
    #                                                                        width=width, cp=cp_al_300, T_i=T_i,
    #                                                                        T_final=T_s, time=delta_t_finite_diff_al)
    # energy_stored_finite_diff_al = (energy_stored_finite_diff_al_per_time *
    #                                 delta_t_finite_diff_al).to(ureg.kjoules / ureg.meters)
    # energy_stored_finite_diff_fireclay_per_time = cf.calc_stored_energy_per_time(rho=rho_fireclay_478,
    #                                                                              thickness=thickness, width=width,
    #                                                                              cp=cp_fireclay_478, T_i=T_i,
    #                                                                              T_final=T_s,
    #                                                                              time=delta_t_finite_diff_fireclay)
    # energy_stored_finite_diff_fireclay = (energy_stored_finite_diff_fireclay_per_time *
    #                                       delta_t_finite_diff_fireclay).to(ureg.kjoules / ureg.meters)
    # energy_stored_finite_diff_cast_iron_per_time = cf.calc_stored_energy_per_time(rho=rho_cast_iron_300,
    #                                                                               thickness=thickness, width=width,
    #                                                                               cp=cp_cast_iron_300, T_i=T_i,
    #                                                                               T_final=T_s,
    #                                                                               time=delta_t_finite_diff_cast_iron)
    # energy_stored_finite_diff_cast_iron = (energy_stored_finite_diff_cast_iron_per_time *
    #                                        delta_t_finite_diff_cast_iron).to(ureg.kjoules / ureg.meters)

    print("The energy stored in the plancha when it reaches 250 degC for each material is as follows... ")
    print("    Lumped Capacitance method, Aluminum: {}".format(round(energy_stored_lumped_al, 2)))
    print("    Lumped Capacitance method, Cast Iron: {}".format(round(energy_stored_lumped_cast_iron, 2)))
    print("    Lumped Capacitance method, Ceramic: {}".format(round(energy_stored_lumped_ceramic, 2)))
    # print("    Finite Difference method, Aluminum: {}".format(round(energy_stored_finite_diff_al, 2)))
    # print("    Finite Difference method, Cast Iron: {}".format(round(energy_stored_finite_diff_cast_iron, 2)))
    # print("    Finite Difference method, Ceramic: {}".format(round(energy_stored_finite_diff_fireclay, 2)))
    print("...")

    """
    Task 3: Determine the heat lost to convection per unit length of the plancha when it has reached 
    operating temperature. You may assume uniform temperature on the top and sides of the 
    plancha for this. 
    """

    conv_loss_per_length = cf.calc_convection_heat_loss(h_value=h_air, thickness=thickness, width=width, T_plancha=T_s,
                                                        T_amb=T_amb).to(ureg.watts / ureg.meters)

    print("The heat lost to convection (per length) when it has reached operating temperature is... ")
    print("    Heat lost to convection, all materials: {}".format(round(conv_loss_per_length, 2)))
    print("...")

    """
    Task 4: If left to continue operating with the stated flux, what would the steady-state temperature 
    of the center of the plancha be for each material?
    """

    T_ss = cf.calc_steady_state_temp(flux=heat_flux, h_value=h_air, width=width, thickness=thickness, T_amb=T_amb).to(ureg.degC)

    conv_loss_at_steady_state_temp = cf.calc_convection_heat_loss(h_value=h_air, thickness=thickness, width=width,
                                                                  T_amb=T_amb, T_plancha=T_ss).to(ureg.watts / ureg.meters)

    print("The steady state temperature for the center of the plancha for each material will be identical... ")
    print("    Steady State Temperature, all materials: {}".format(round(T_ss, 2)))
    print("    The heat lost at steady state temperature is: {}".format(round(conv_loss_at_steady_state_temp, 2)))
    print("...")

    """
    Task 5: Once the plancha reaches a uniform temperature of 250°C at the initial flux, to what value 
    should the firepower (applied flux) be reduced to achieve a constant cooking temperature 
    at 250°C? You may assume uniform temperature on the top and sides of the plancha. 
    """

    steady_state_flux_250 = cf.calc_convection_heat_loss(h_value=h_air, thickness=thickness, width=width, T_amb=T_amb,
                                                         T_plancha=T_s)

    print("The flux required for steady state temperature at 250 C will be identical for each material... ")
    print("    Steady State Applied Flux, all materials: {}".format(round(steady_state_flux_250, 2)))
    print("...")

    """
    Task 6: If the convective heat transfer coefficient is reduced by half, how is the time to heat up to 
    250°C changed?
    """

    # METHOD 1: LUMPED CAPACITANCE

    delta_t_lumped_al_half_h = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air/2, rho=rho_al_300,
                                                          thickness=thickness, width=width, cp=cp_al_300,
                                                          flux=heat_flux, T_final=T_s).to(ureg.seconds)
    delta_t_lumped_fireclay_half_h = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air/2,
                                                                rho=rho_fireclay_478, thickness=thickness, width=width,
                                                                cp=cp_fireclay_478, flux=heat_flux,
                                                                T_final=T_s).to(ureg.seconds)
    delta_t_lumped_cast_iron_half_h = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air/2,
                                                                 rho=rho_cast_iron_300, thickness=thickness,
                                                                 width=width, cp=cp_cast_iron_300, flux=heat_flux,
                                                                 T_final=T_s).to(ureg.seconds)

    # # METHOD 2: FINITE DIFFERENCE
    #
    # bi_al_half_h = cf.calc_biot(h_value=0.5*h_air, k_value=k_al_300, thickness=thickness)
    # dt_al_half_h = cf.stability_analysis(h_value=0.5*h_air, k_value=k_al_300, thickness=thickness, rho=rho_al_300,
    #                                      cp=cp_al_300, dx=dx)
    # delta_t_finite_diff_al_half_h = cf.calc_finite_difference(fo=fo_al, biot=bi_al_half_h, T_i=T_i, flux=heat_flux,
    #                                                           k_value=k_al_300, thickness=thickness, width=width,
    #                                                           T_amb=T_amb, dx=dx, dt=dt_al_half_h, T_s=T_s)
    # biot_fireclay_half_h = cf.calc_biot(h_value=0.5*h_air, k_value=k_fireclay_478, thickness=thickness)
    # dt_fireclay_half_h = cf.stability_analysis(h_value=0.5*h_air, k_value=k_fireclay_478, thickness=thickness,
    #                                            rho=rho_fireclay_478, cp=cp_fireclay_478, dx=dx)
    # delta_t_finite_diff_fireclay_half_h = cf.calc_finite_difference(fo=fo_fireclay, biot=biot_fireclay_half_h, T_i=T_i,
    #                                                                 flux=heat_flux, k_value=k_fireclay_478,
    #                                                                 thickness=thickness, width=width, T_amb=T_amb,
    #                                                                 dx=dx, dt=dt_fireclay_half_h, T_s=T_s)
    # biot_cast_iron_half_h = cf.calc_biot(h_value=h_air*0.5, k_value=k_cast_iron_300, thickness=thickness)
    # dt_cast_iron_half_h = cf.stability_analysis(h_value=0.5*h_air, k_value=k_cast_iron_300, thickness=thickness,
    #                                             rho=rho_cast_iron_300, cp=cp_cast_iron_300, dx=dx)
    # delta_t_finite_diff_cast_iron_half_h = cf.calc_finite_difference(fo=fo_cast_iron, biot=biot_cast_iron_half_h,
    #                                                                  T_i=T_i, flux=heat_flux, k_value=k_cast_iron_300,
    #                                                                  thickness=thickness, width=width, T_amb=T_amb,
    #                                                                  dx=dx, dt=dt_cast_iron_half_h, T_s=T_s)

    print("The time to heat to 250 degC for each material with the convective heat transfer coefficient halved is... ")
    print("    Lumped Capacitance method, Aluminum: {}".format(round(delta_t_lumped_al_half_h, 2)))
    print("    Lumped Capacitance method, Cast Iron: {}".format(round(delta_t_lumped_cast_iron_half_h, 2)))
    print("    Lumped Capacitance method, Ceramic: {}".format(round(delta_t_lumped_fireclay_half_h, 2)))
    # print("    Finite Difference method, Aluminum: {}".format(round(delta_t_finite_diff_al_half_h, 2)))
    # print("    Finite Difference method, Cast Iron: {}".format(round(delta_t_finite_diff_cast_iron_half_h, 2)))
    # print("    Finite Difference method, Ceramic: {}".format(round(delta_t_finite_diff_fireclay_half_h, 2)))
    print("...")

    temp_at_half_time_to_op_temp_al = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air, rho=rho_al_300,
                                                                 thickness=thickness, width=width, cp=cp_al_300,
                                                                 flux=heat_flux, time=delta_t_lumped_al*0.5).to(ureg.degC)
    temp_at_half_time_to_op_temp_cast_iron = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air,
                                                                        rho=rho_cast_iron_300, thickness=thickness,
                                                                        width=width, cp=cp_cast_iron_300,
                                                                        flux=heat_flux, time=delta_t_lumped_cast_iron*0.5).to(ureg.degC)
    temp_at_half_time_to_op_temp_fireclay = cf.calc_lumped_capacitance(T_amb=T_amb, T_i=T_i, h_value=h_air,
                                                                       rho=rho_fireclay_478, thickness=thickness,
                                                                       width=width, cp=cp_fireclay_478, flux=heat_flux,
                                                                       time=delta_t_lumped_fireclay*0.5).to(ureg.degC)

    print("Plancha temp at half the time to operating temp:")
    print("    Aluminum: {}".format(round(temp_at_half_time_to_op_temp_al, 2)))
    print("    Cast Iron: {}".format(round(temp_at_half_time_to_op_temp_cast_iron, 2)))
    print("    Ceramic: {}".format(round(temp_at_half_time_to_op_temp_fireclay, 2)))
    print("...")

    print("dx = {}".format(dx))
    print("aluminum dt = {}".format(dt_al))
    print("cast iron dt = {}".format(dt_cast_iron))
    print("ceramic dt = {}".format(dt_fireclay))


if __name__ == "__main__":
    main()
