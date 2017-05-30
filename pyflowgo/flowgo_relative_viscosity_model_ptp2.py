import math
import json
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_vesicle_fraction_model_bimodal

import pyflowgo.base.flowgo_base_relative_viscosity_model


class FlowGoRelativeViscosityModelPhanThienPham2(pyflowgo.base.flowgo_base_relative_viscosity_model.
                                                 FlowGoBaseRelativeViscosityModel):
    """This methods permits to calculate the effect of crystals and bubbles cargo on viscosity according to
    Phan‐Thien and Pham [1997]. They propose a treatment for the viscosity of a three‐phase mixture
    comprising a suspension of rigid spherical particles and bubbles.
    Here the method ptp2 corresponds to case 2 from Phan‐Thien and Pham [1997] where:
    Crystals and bubbles are of the same size range.
    The input parameters include the crystal fraction (phi) and the bubbles fraction (vesicle_fraction retrieved from
    the vesicle_fraction_model) """

    def __init__(self, vesicle_fraction_model=None):
        super().__init__()

        if vesicle_fraction_model == None:
            self._vesicle_fraction_model = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        else:
            self._vesicle_fraction_model = vesicle_fraction_model

    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)

    def compute_relative_viscosity(self, state):
        phi = state.get_crystal_fraction()
        # here the vesicle model is directly called
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)

        relative_viscosity = math.pow((1. - phi - vesicle_fraction),-((5. * phi + 2. * vesicle_fraction) / (2. * (phi + vesicle_fraction))))
        return relative_viscosity


#### NEED TO WRITE THE LIMITING CONDITION HERE: stop when when phi = 0.52
