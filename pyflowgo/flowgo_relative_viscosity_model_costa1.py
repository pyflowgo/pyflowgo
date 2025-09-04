# Copyright 2017 PyFLOWGO development team (Magdalena Oryaelle Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFLOWGO library.
#
# The PyFLOWGO library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The PyFLOWGO library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License
# along with the PyFLOWGO library.  If not, see https://www.gnu.org/licenses/.

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
    Cimarelli, C., A. Costa, S. Mueller, and H. M. Mader (2011), Rheology of magmas with bimodal crystal size and shape
    distributions: Insights from analog experiments, Geochem. Geophys. Geosyst., 12, Q07024, doi:10.1029/2011GC003606.

    Costa, A., L. Caricchi, and N. Bagdassarov (2009), A model for the rheology of particle‐bearing suspensions
    and partially molten rocks, Geochem. Geophys. Geosyst., 10, Q03010, doi:10.1029/2008GC002138.
    """


    def __init__(self) -> None:
        super().__init__()

        self._strain_rate = 1.

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._strain_rate = float(data['relative_viscosity_parameters']['strain_rate'])

    def compute_relative_viscosity(self, state):

        phi = state.get_crystal_fraction()
        #strain_rate = state.get_strain_rate()
        if self._strain_rate == 1.0:
        #if strain_rate >= 1.0:
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
        #if strain_rate == 0.0001:
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

    def is_notcompatible(self, state):
        return False