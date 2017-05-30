import math
import json

import pyflowgo.base.flowgo_base_relative_viscosity_model


class FlowGoRelativeViscosityModelMP(pyflowgo.base.flowgo_base_relative_viscosity_model.
                                     FlowGoBaseRelativeViscosityModel):
    """This methods permits to calculate the effect of crystal cargo on viscosity according to the Maron-Pierce []
    relationship. This relationship has only the maximum packing (phimax, φm) as adjustable parameter.
    This relationship differs from the Krieger-Dougherty [] equation because B (beinstein) is not a fit parameter,
    but is calculated from the relationship Bφm = 2
    The input parameters include the variable crystal fraction (phi) and the maximum packing (phimax)"""

    _phimax = 0.633

    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            self._phimax = float(data['relative_viscosity_parameters']['max_packing'])

    def compute_relative_viscosity(self, state):
        phi = state.get_crystal_fraction()

        relative_viscosity = math.pow((1. - 1/self._phimax * phi), - 2.)
        return relative_viscosity
