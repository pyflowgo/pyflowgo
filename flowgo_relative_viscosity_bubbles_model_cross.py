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
import pyflowgo.flowgo_material_lava

import pyflowgo.base.flowgo_base_relative_viscosity_bubbles_model


class FlowGoRelativeViscosityBubblesModelCross(pyflowgo.base.flowgo_base_relative_viscosity_bubbles_model.
                                     FlowGoBaseRelativeViscosityBubblesModel):
    """This methods permits to calculate the effect of undeformable bubbles on viscosity:
    they act as rigid spheres and increase bulk viscosity:

    Input data
    -----------
    The vesicle fraction in the json file as either a single value (float or int), or as a list with the structure
    [[r1,w1],[r2,w2],...[rn,wn]]
    where ri is a bubble radius and wi is the fraction of bubbles of this size. The sum of all w should equal 1.

    Variables
    -----------
    The vesicle fraction

    Returns
    ------------
    The effect of elongated bubbles on viscosity

    References
    ---------
    Llewellin, E.W., Manga, M., 2005. Bubble suspension rheology and implications for conduit flow.
    Journal of Volcanology and Geothermal Research 143, 205–217. http:// dx.doi.org/10.1016/j.jvolgeores.2004.09.018.
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
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

        self._radius = data['relative_viscosity_parameters']['radius']
        self._surfacetension = float(data['relative_viscosity_parameters']['surface_tension'])

    def compute_relative_viscosity_bubbles(self, state):
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)
        strain_rate = state.get_strain_rate()
        melt_viscosity = self._melt_viscosity_model.compute_melt_viscosity(state)

        relative_viscosity_inf = math.pow((1. - vesicle_fraction), 5/3.)
        relative_viscosity_0 = math.pow((1. - vesicle_fraction), - 1.)

        D = 1e-15
        if type(self._radius) != list:
            size = self._radius
            Ca = size * strain_rate * melt_viscosity / self._surfacetension
            D = 1 / (1 + math.pow(6 / 5 * Ca, 2))

        else:
            for size,w in self._radius:
                Ca = size * strain_rate * melt_viscosity / self._surfacetension
                D += w/(1+math.pow(6/5*Ca,2))

        relative_viscosity_bubbles = relative_viscosity_inf + (relative_viscosity_0 - relative_viscosity_inf)*D

        return relative_viscosity_bubbles

