import math
import json

import pyflowgo.base.flowgo_base_relative_viscosity_model


class FlowGoRelativeViscosityModelCosta1(pyflowgo.base.flowgo_base_relative_viscosity_model.
                                         FlowGoBaseRelativeViscosityModel):

    """This methods permits to calculate the effect of crystal cargo on viscosity according to Costa et al []
    This relationship considers the strain rate and allows to evalutate the effect of high crystal fraction
    (above maximum packing).
    The input parameters include the variable crystal fraction (phi) and other parameters depending on the aspect ratio
    of the crystals.
    Here the method costa1 corresponds to case where:
    all crystals are spherical
    for strain-rate = 1s-1, phi_max = 0.61
    for strain-rate = 10-4 s-1, phi_max= 0.54,

    The inputs parameters correspond to the particles A from Cimarelli et al. [2011]

    References:
    ---------


    """


    _strain_rate = 1.

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._strain_rate = float(data['relative_viscosity_parameters']['strain_rate'])

    def compute_relative_viscosity(self, state):

        phi = state.get_crystal_fraction()
        if self._strain_rate == 1.0:
            # for spheres, A particles from Cimarelli et al., 2011
            # self.phi_max = 0.61,
            delta_1 = 11.4
            gama_1 = 1.6
            phi_star_1 = 0.67
            epsilon_1 = 0.01

            f = (1. - epsilon_1) * math.erf(min(25., (
                (math.sqrt(math.pi) / (2. * (1. - epsilon_1))) * (phi / phi_star_1) * (
                    1. + (math.pow((phi / phi_star_1), gama_1))))))

            relative_viscosity = (1. + math.pow((phi / phi_star_1), delta_1)) / (
                math.pow((1. - f), (2.5 * phi_star_1)))
            return relative_viscosity

        if self._strain_rate == 0.0001:
            # spheres A particles from Cimarelli et al., 2011
            # self.phi_max_1 = 0.54,
            delta_1 = 11.48
            gama_1 = 1.52
            phi_star_1 = 0.62
            epsilon_1 = 0.005

            f = (1. - epsilon_1) * math.erf(min(25., (
                (math.sqrt(math.pi) / (2. * (1. - epsilon_1))) * (phi / phi_star_1) * (
                    1. + (math.pow((phi / phi_star_1), gama_1))))))

            relative_viscosity = (1. + math.pow((phi / phi_star_1), delta_1)) / (
                math.pow((1. - f), (2.5 * phi_star_1)))
            return relative_viscosity


