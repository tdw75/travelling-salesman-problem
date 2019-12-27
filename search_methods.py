from problem_set_up import *
import time


class TwoOpt(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)

    def identify_orientation(self):
        pass

    def find_intersecting_edges(self):
        pass

    def two_opt_swap(self):
        pass

    def search(self):
        pass


class IteratedGreedy(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class SimulatedAnnealing(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class TabuSearch(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)
