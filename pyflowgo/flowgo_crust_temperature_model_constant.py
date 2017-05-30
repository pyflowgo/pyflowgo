import json


import pyflowgo.base.flowgo_base_crust_temperature_model


class FlowGoCrustTemperatureModelConstant(pyflowgo.base.flowgo_base_crust_temperature_model.
                                          FlowGoBaseCrustTemperatureModel):
    """
        This method "constant" considers constant temperature of the crust downflow that is set to be the
        initial_crust_temperature in the json file.

        Input data
        -----------
        json file containing the crust_temperature

        Returns
        ------------
        crust temperature in K

    """

    _crust_temperature = 425 + 273.15

    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            self._crust_temperature = float(data['thermal_parameters']['crust_temperature'])

    def compute_crust_temperature(self, state):
        return self._crust_temperature

