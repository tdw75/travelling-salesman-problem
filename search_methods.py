from initial_solutions import *
from problem_set_up import calculate_tour_length


def anti_clockwise(a, b, c):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def two_opt_swap(tour, i, j):
    if i < j:
        route = tour[:i]
        reversed_section = tour[i:j + 1]
        reversed_section.reverse()
        route += reversed_section
        route += tour[j + 1:]
    else:
        route = tour[j + 1:i]
        reversed_section = tour[i:] + tour[:j + 1]
        reversed_section.reverse()
        route += reversed_section

    return route


def metropolis(tour_old, tour_new, obj_old, obj_new, temp):
    delta = obj_new - obj_old
    prob = np.exp(-delta / temp)

    if obj_new <= obj_old:
        return tour_new, obj_new
    elif np.random.rand() <= prob:
        return tour_new, obj_new
    else:
        return tour_old, obj_old


class TwoOpt(InitialSolution):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.intersecting_edges = None

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

    def search(self, max_iterations):

        for iteration in range(max_iterations):
            i = np.random.randint(self.node_count)
            j = np.random.randint(self.node_count)

            if abs(i - j) <= 1:
                continue

            start = min(i, j)
            end = max(i, j)

            tour = two_opt_swap(self.tour, start, end)
            if calculate_tour_length(tour, self.dist_matrix, self.node_count) < self.obj_value:
                self.tour = tour

        calculate_tour_length(self.tour, self.dist_matrix, self.node_count)


def cities_to_swap(node_count):
    i = np.random.randint(node_count)
    j = np.random.randint(node_count)

    if i == j:
        i, j = cities_to_swap(node_count)

    return i, j


class SimulatedAnnealing(InitialSolution):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.search_iterations = 0
        self.obj_tracker = []

    def search(self, inital_temp, cooling_rate):
        temp = inital_temp

        iterations = 0
        self.obj_tracker = []

        while temp > 1:
            i, j = cities_to_swap(self.node_count)

            tour_new = two_opt_swap(self.tour, i, j)
            tour_old = self.tour
            obj_old = self.obj_value
            obj_new = calculate_tour_length(tour_new, self.dist_matrix, self.node_count)

            self.tour, self.obj_value = metropolis(tour_old, tour_new, obj_old, obj_new, temp)
            self.obj_tracker.append(self.obj_value)
            temp *= 1 - cooling_rate
            iterations += 1

        self.search_iterations = iterations


class IteratedGreedy(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class TabuSearch(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)
