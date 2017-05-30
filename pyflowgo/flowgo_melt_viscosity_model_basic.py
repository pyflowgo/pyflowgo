import math
import json
import pyflowgo.base.flowgo_base_melt_viscosity_model


class FlowGoMeltViscosityModelBasic(pyflowgo.base.flowgo_base_melt_viscosity_model.FlowGoBaseMeltViscosityModel):

    """ This function calculates the viscosity of the melt according to the original FLOWGO from Harris and Rowland 2001
    where the viscosity is calculated via Dragoni (1989)

    viscosity(Pa.s)(T) = viscosity_eruption * a(eruption_temperature -  core_temperature),
    for core_temperature < eruption_temperature

    where a is a constant given by Dragoni (1986) = 0.04 ° K-1

    Input data
    -----------
    json file containing the viscosity_eruption  and eruption_temperature

    variables
    -----------
    temperature of the lava interior : core_temperature

    Returns
    ------------
    the viscosity of the pure melt in Pa.s

    Reference
    ---------
    Dragoni M. (1989) A dynamical model of lava flows cooling by radiation. Bull Volcanol, 51:88-95

    """
    _viscosity_eruption = 1000.
    _eruption_temperature = 1137. + 273.15

    # faire le test de bien lire ces valeurs
    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

            self._viscosity_eruption = float(data['eruption_condition']['viscosity_eruption'])
            self._eruption_temperature = float(data['eruption_condition']['eruption_temperature'])

    def compute_melt_viscosity(self, state):
        a = 0.04

        core_temperature = state.get_core_temperature()

        melt_viscosity = self._viscosity_eruption * math.exp(a * (self._eruption_temperature - core_temperature))
        #print('viscosity',melt_viscosity)
        return melt_viscosity
