from problem_set_up import *


class NearestNeighbour(TspSetUp):
    def __init__(self, input_data):
        TspSetUp.__init__(self, input_data)

    def solve(self, starting_node):
        unvisted_nodes = list(self.dist_matrix.keys())
        current_node = starting_node
        while unvisted_nodes:
            pass

    def save_solution(self):
        pass

    def calculate_tour_length(self):
        pass
