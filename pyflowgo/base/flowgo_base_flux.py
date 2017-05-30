# from abc import ABC, abstractmethod -> python 3.4
from abc import ABCMeta, abstractmethod


class FlowGoBaseFlux(metaclass=ABCMeta):
    @abstractmethod
    def read_initial_condition_from_json_file(self, filename):
        pass

    @abstractmethod
    def compute_flux(self, state, channel_width, channel_depth):
        pass
