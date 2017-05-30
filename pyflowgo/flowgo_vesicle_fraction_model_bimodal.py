import json

import pyflowgo.base.flowgo_base_vesicle_fraction_model


class FlowGoVesicleFractionModelBimodal(pyflowgo.base.flowgo_base_vesicle_fraction_model.
                                        FlowGoBaseVesicleFractionModel):

    # For Mauna Loa 1859
    _critical_distance = 10000.
    _vesicle_fraction_1 = 0.4
    _vesicle_fraction_2 = 0.1


    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

            if 'critical_distance' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['critical_distance'] entry in json")

            if 'vesicle_fraction_1' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['vesicle_fraction_1'] entry in json")

            if 'vesicle_fraction_2' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['vesicle_fraction_2'] entry in json")

            self._critical_distance = float(data['lava_state']['critical_distance'])
            self._vesicle_fraction_1 = float(data['lava_state']['vesicle_fraction_1'])
            self._vesicle_fraction_2 = float(data['lava_state']['vesicle_fraction_2'])


    def computes_vesicle_fraction(self, state):
        current_position = state.get_current_position()

        if current_position <= self._critical_distance:
            return self._vesicle_fraction_1
        else:
            return self._vesicle_fraction_2