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

import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_vesicle_fraction_model_bimodal
import pyflowgo.base.flowgo_base_relative_viscosity_model
import pyflowgo.flowgo_material_lava

class FlowGoRelativeViscosityModelBLL(pyflowgo.base.flowgo_base_relative_viscosity_model.
                                     FlowGoBaseRelativeViscosityModel):
    """
    This function calculates the effect of crystal and bubble cargo on viscosity using the model of Birnbaum,
    Lev, and Llewellin (2021):

    relative_viscosity = (1. - (phi / (self._phimax*(1. - vesicle_fraction)))) ** (-self._einstein) * \
                             (1. - vesicle_fraction) ** (-self._beinstein) * ((strain_rate) ** (n - 1))

    on the basis of analogue experiments where phimax was 0.56, einstein was 2.74, beinstein was 1.98, and n was
    given by:
     n = { 1, for self._phimax*(1. - vesicle_fraction) + vesicle_fraction<=phicrit;
          1 + (0.7 - 0.55*Ca) * (phicrit - phi - vesicle_fraction) for
                  self._phimax*(1. - vesicle_fraction) + vesicle_fraction>phicrit
    where phicrit was measured to be 0.39, and Ca is the capillary number:
    Ca = self._radius*strain_rate*melt_viscosity/self._surfacetension

    Input data
    -----------
    maximum packing for particles (phimax)
    einstein exponent for particles (einstein)
    einstein exponent for bubbles (beinstein)
    critical packing fractions for particles and bubbles (phicrit)
    bubble radius (radius)
    surface tension of vapor bubbles in melt (surfacetension)

    variables
    -----------
    crystal fraction: phi
    vesicle fraction: vesicle_fraction
    strain rate: strain_rate
    melt viscosity: melt_viscosity

    Returns
    ------------
    the relative viscosity due to the crystal and bubble cargo

    Reference
    ---------

    Birnbaum, J., Lev, E., Llewellin, E. W. (2021) Rheology of three-phase suspensions determined
    via dam-break experiments. Proc. R. Soc. A 477 (20210394): 1-16.

    """

    def __init__(self, vesicle_fraction_model=None, melt_viscosity_model=None):
        super().__init__()

        if vesicle_fraction_model == None:
            self._vesicle_fraction_model = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        else:
            self._vesicle_fraction_model = vesicle_fraction_model

        if melt_viscosity_model == None:
            self._melt_viscosity_model = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        else:
            self._melt_viscosity_model = melt_viscosity_model


    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            self._phimax = float(data['relative_viscosity_parameters']['max_packing'])
            self._phicrit = float(data['relative_viscosity_parameters']['crit_packing'])
            self._einstein = float(data['relative_viscosity_parameters']['einstein_coef'])
            self._beinstein = float(data['relative_viscosity_parameters']['beinstein_coef'])
            self._radius = float(data['relative_viscosity_parameters']['radius'])
            self._surfacetension = float(data['relative_viscosity_parameters']['surface_tension'])

    def compute_relative_viscosity(self, state):
        phi = state.get_crystal_fraction()
        strain_rate = state.get_strain_rate()
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)
        melt_viscosity = self._melt_viscosity_model.compute_melt_viscosity(state)

        n = 1
        if (phi + vesicle_fraction) >= self._phicrit:
            Ca = self._radius * strain_rate * melt_viscosity / self._surfacetension
            n = 1 + (0.7 - 0.55 * Ca) * (self._phicrit - phi - vesicle_fraction)

        relative_viscosity = (1. - (phi / (self._phimax * (1. - vesicle_fraction)))) ** (-self._einstein) * \
                             (1. - vesicle_fraction) ** (-self._beinstein) * ((strain_rate) ** (n - 1))

        return relative_viscosity

    def is_notcompatible(self, state):
        phi = state.get_crystal_fraction()
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)

        if phi > (self._phimax * (1 - vesicle_fraction)):
            return True
        else:
            return False
