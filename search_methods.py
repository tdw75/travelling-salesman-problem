from problem_set_up import *
from initial_solutions import *
import time


def anti_clockwise(a, b, c):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


class TwoOpt(NearestNeighbour):
    def __init__(self, input_data, initial_solution):
        super().__init__(input_data)
        self.initial_solution = initial_solution
        self.initial_solutions = ['nearest neighbour', 'sequential tour', 'random tour']
        self.intersecting_edges = None

    def generate_initial_solution(self):

        if self.initial_solution not in self.initial_solutions:
            raise ValueError()

        if self.initial_solution == "nearest neighbour":
            self.nn_initial_solution(starting_node=np.random.randint(self.node_count))
        if self.initial_solution == "sequential tour":
            self.trivial_tour()
        if self.initial_solution == 'random tour':
            self.random_tour()

    def intersect(self, edge1, edge2):

        p1 = self.coordinates[edge1[0]]
        q1 = self.coordinates[edge1[1]]
        p2 = self.coordinates[edge2[0]]
        q2 = self.coordinates[edge2[1]]

        return anti_clockwise(p1, p2, q2) != anti_clockwise(q1, p2, q2) and \
               anti_clockwise(p1, q1, p2) != anti_clockwise(p1, q1, q2)

    def find_intersecting_edges(self):

        self.intersecting_edges = {}

        start = 1

        for edge1 in self.edges[:-1]:
            self.intersecting_edges[edge1] = []

            for edge2 in self.edges[start:]:
                if edge1[0] not in edge2 and edge1[1] not in edge2:
                    if self.intersect(edge1, edge2):
                        self.intersecting_edges[edge1].append(edge2)

            if not self.intersecting_edges[edge1]:
                del self.intersecting_edges[edge1]

            start += 1

        print(start)

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
