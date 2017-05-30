# from abc import ABC, abstractmethod -> python 3.4
from abc import ABCMeta, abstractmethod


class FlowGoBaseYieldStrengthModel(metaclass=ABCMeta):
    @abstractmethod
    def read_initial_condition_from_json_file(self, filename):
        pass

    @abstractmethod
    def compute_yield_strength(self, state, eruption_temperature):
        pass

    @abstractmethod
    def compute_basal_shear_stress(self, state, terrain_condition, material_lava):
        pass
