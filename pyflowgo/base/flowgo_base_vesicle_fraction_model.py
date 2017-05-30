# from abc import ABC, abstractmethod -> python 3.4
from abc import ABCMeta, abstractmethod


class FlowGoBaseVesicleFractionModel(metaclass=ABCMeta):
    @abstractmethod
    def read_initial_condition_from_json_file(self, filename):
        pass

    @abstractmethod
    def computes_vesicle_fraction(self, state):
        pass
