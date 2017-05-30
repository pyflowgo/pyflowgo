import math
import json

import pyflowgo.base.flowgo_base_melt_viscosity_model


class FlowGoMeltViscosityModelShaw(pyflowgo.base.flowgo_base_melt_viscosity_model.FlowGoBaseMeltViscosityModel):

    """ This function calculates the viscosity of teh melt according to Shaw et al. 1972:

    ln viscosity(Poise) = slope*(10000/T(K))-(1.5*slope)-6.4

    where slope is the intercept calculated from the chemical composotion of the silicate liquid

    Input data
    -----------
    json file containing the shaw_slope in melt_viscosity_parameters

    variables
    -----------
    temperature of the lava interior : core_temperature

    Returns
    ------------
    the viscosity of the pure melt in Pa.s

    References
    ---------
    Shaw (1972). Viscosity of magmatic silicate liquids: an empirical method of prediction.
    American Journal of science, Vol. 272, p. 870-893.

    """

    _shaw_slope = 2.36

    # faire le test de bien lire ces valeurs
    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

            self._shaw_slope = float(data['melt_viscosity_parameters']['shaw_slope'])

    def compute_melt_viscosity(self, state):

        core_temperature = state.get_core_temperature()

        melt_viscosity = 10 ** (((self._shaw_slope * (10000. / core_temperature) - (1.5 * self._shaw_slope) - 6.4) / 2.303) - 1)

        return melt_viscosity
