# from abc import ABC, abstractmethod -> python 3.4
from abc import ABCMeta, abstractmethod


class FlowGoBaseCrystallizationRateModel(metaclass=ABCMeta):
    @abstractmethod
    def read_initial_condition_from_json_file(self, filename):
        pass

    @abstractmethod
    def get_crystal_fraction(self,temperature):
        pass

    @abstractmethod
    def compute_crystallization_rate(self, state):
        pass

    @abstractmethod
    def get_solid_temperature(self):
        pass
