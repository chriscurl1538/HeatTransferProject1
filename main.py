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


# Declare constants

width = 45 * ureg.cm
thickness = 1 * ureg.cm
heat_flux = Q_(4500, ureg.Watts / ureg.meter**2)    # Biomass fire

T_amb = 27 * ureg.Celsius
h_air = Q_(15, ureg.Watts / (ureg.meter**2 * ureg.Kelvin))
T_i = 305 * ureg.Kelvin
T_s = 250 * ureg.Celsius     # Operating Temp

# Material properties (478K) - Ceramic "Fireclay brick"
rho_fireclay_478 = Q_(2645, ureg.kg / ureg.meters**3)
cp_fireclay_478 = Q_(960, ureg.Joules / (ureg.kg * ureg.Kelvin))
k_fireclay_478 = Q_(1, ureg.Watts / (ureg.meters / ureg.Kelvin))

# Material properties (300K) - Cast iron "plain carbon steel"
rho_cast_iron_300 = Q_(7854, ureg.kg / ureg.meters**3)
cp_cast_iron_300 = Q_(434, ureg.Joules / (ureg.kg * ureg.Kelvin))
k_cast_iron_300 = Q_(60.5, ureg.Watts / (ureg.meters / ureg.Kelvin))
alpha_cast_iron_300 = Q_(17.7 * 10**6, ureg.meters**2 / ureg.seconds)

# Material properties (300K) - Aluminum
rho_al_300 = Q_(2702, ureg.kg / ureg.meters**3)
cp_al_300 = Q_(903, ureg.Joules / (ureg.kg * ureg.Kelvin))
k_al_300 = Q_(237, ureg.Watts / (ureg.meters / ureg.Kelvin))
alpha_al_300 = Q_(97.1 * 10**6, ureg.meters**2 / ureg.seconds)
