import math
import json

import pyflowgo.base.flowgo_base_effective_cover_crust_model


class FlowGoEffectiveCoverCrustModelBasic(pyflowgo.base.flowgo_base_effective_cover_crust_model.
                                          FlowGoBaseEffectiveCoverCrustModel):

    """
     This method "basic" allows to calculate the effective cover fraction (f_crust) as a function of velocity fallowing
    Harris & Rowland (2001):
    f_crust = fc * math.exp(alpha * v_mean)

    where fc is the crust_cover_fraction that is either equals to 1 or is comprise between 0 and 1


    Harris and Rowland [2001] give fc  = 0.9 and alpha = – 0.16 for a poorly insulated flow
    and fc = 1.0 and  alpha = – 0.00756 for a more heavily crusted flow.
    Alternatively, crust cover can be set to be constant down-channel if and alpha = 0 f_crust will stay constant and
    equals to fc that can be set between zero (crust free, poorly insulated) and unity
    (complete crust coverage, well insulated).

    Note that complete crustal coverage is not equivalent to flow in a lava tube [Rowland et al., 2005].

    Input data
    -----------
    from the json file:
    the crust_cover fraction
    alpha

    Returns
    ------------
    the effective crust cover fraction, that is the amount of crust that cover the hot lava in the channel
    (more cover fraction; more isolated is the channel and therefore it cools less.

    References
    -------------
    Rowland, S., H. Garbeil, and A. Harris (2005), Lengths and hazards from channel‐fed lava flows on Mauna Loa,
    Hawai‘i, determined from thermal and downslope modeling with FLOWGO, Bull. Volcanol., 67, 634–647.

    """

    _alpha = -7.56e-3
    _crust_cover_fraction = 0.9

    def __init__(self, terrain_condition, material_lava):
        self._material_lava = material_lava
        self._terrain_condition = terrain_condition

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._alpha = float(data['thermal_parameters']['alpha'])
            self._crust_cover_fraction = float(data['thermal_parameters']['crust_cover_fraction'])

    def compute_effective_cover_fraction(self, state):

        #  TODO Is it ok to call the v_mean like this ?
        v_mean = self._material_lava.compute_mean_velocity(state, self._terrain_condition)

        effective_cover_fraction = self._crust_cover_fraction * math.exp(self._alpha * v_mean)

        return effective_cover_fraction
