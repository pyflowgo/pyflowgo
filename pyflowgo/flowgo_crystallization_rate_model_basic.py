import json

import pyflowgo.base.flowgo_base_crystallization_rate_model


class FlowGoCrystallizationRateModelBasic(pyflowgo.base.flowgo_base_crystallization_rate_model.
                                          FlowGoBaseCrystallizationRateModel):
    """
        This model called "basic" calculates the amount of crystal (in fraction) as a function of the amount of cooling
        as suggested by Harris and Rowland (2001).
        It take into account the amount of crystallization during the eruption that occurred between the eruption
        temperature and the solid temperature (temperature at which the material cannot flow anymore)

        Input data
        -----------
        json file containing:
        initial crystal_fraction,
        crystals_grown_during_cooling,
        solid_temperature
        eruption_temperature

        Returns
        ------------
        the crystallization rate in fraction of crystals per degree

        """

    _crystal_fraction = 0.15
    _crystals_grown_during_cooling = 0.45
    _solid_temperature = 990. + 273.15
    _eruption_temperature = 1137. + 273.15

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._crystal_fraction = float(data['lava_state']['crystal_fraction'])
            self._crystals_grown_during_cooling = float(data['crystals_parameters']['crystals_grown_during_cooling'])
            self._solid_temperature = float(data['crystals_parameters']['solid_temperature'])
            self._eruption_temperature = float(data['eruption_condition']['eruption_temperature'])

    def get_crystal_fraction(self, temperature):
        return self._crystal_fraction

    def compute_crystallization_rate(self, state):
        crystallization_rate = self._crystals_grown_during_cooling / (self._eruption_temperature -
                                                                      self._solid_temperature)
        return crystallization_rate

    def get_solid_temperature(self):
        return self._solid_temperature
