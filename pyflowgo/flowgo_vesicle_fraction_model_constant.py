import json
import pyflowgo.base.flowgo_base_vesicle_fraction_model

class FlowGoVesicleFractionModelConstant(pyflowgo.base.flowgo_base_vesicle_fraction_model.
                                        FlowGoBaseVesicleFractionModel):
    # TODO: comment the function

    # this is the Volume fraction considered constant along the flow
    _vesicle_fraction = 0.1

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._vesicle_fraction = float(data['lava_state']['vesicle_fraction'])

    def computes_vesicle_fraction(self, state):
        vesicle_fraction = self._vesicle_fraction
        return vesicle_fraction

