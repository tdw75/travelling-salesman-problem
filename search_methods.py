from initial_solutions import *
from problem_setup import calculate_tour_length


def anti_clockwise(a, b, c):
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def cities_to_swap(node_count):
    i = np.random.randint(node_count)
    j = np.random.randint(node_count)

    if i == j:
        i, j = cities_to_swap(node_count)

    return i, j


def two_opt_swap(tour, i, j, node_count=None):
    if node_count:
        n = node_count
    else:
        n = len(tour)
    j = n + j if j < 0 else j
    i = n + i if i < 0 else i

    if i <= j:
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


def greedy_two_opt(tour, obj, dist_matrix, node_count, k=25):
    obj_best = obj
    tour_best = tour

    for idx in tour:

        start_idx = idx - k
        end_idx = idx + k
        if start_idx >= 0:
            nodes = tour_best[start_idx:end_idx + 1]
        else:
            nodes = tour_best[start_idx:] + tour_best[:end_idx + 1]

        for node in nodes:
            tour_temp = two_opt_swap(tour_best, idx, node, node_count)
            obj_temp = calculate_tour_length(tour_temp, dist_matrix, node_count)

            if obj_temp < obj_best:
                tour_best = tour_temp
                obj_best = obj_temp

    return tour_best, obj_best


def metropolis(tour_old, tour_new, obj_old, obj_new, temp):
    delta = obj_new - obj_old
    prob = np.exp(-delta / temp)

    if obj_new <= obj_old:
        return tour_new, obj_new
    elif np.random.rand() <= prob:
        return tour_new, obj_new
    else:
        return tour_old, obj_old


class IteratedTwoOpt(InitialSolution):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.search_iterations = 0
        self.improvement = None

    def search(self, k=50):

        if not self.tour:
            raise ValueError("No initial solution has been set")

        tour_new, obj_new = greedy_two_opt(self.tour, self.obj_value, self.dist_matrix, self.node_count, k=k)
        improvement = self.obj_value - obj_new
        self.tour, self.obj_value = tour_new, obj_new
        self.obj_tracker.append(self.obj_value)

        while improvement > 0:
            tour_new, obj_new = greedy_two_opt(self.tour, self.obj_value, self.dist_matrix, self.node_count, k=k)
            improvement = self.obj_value - obj_new
            self.tour, self.obj_value = tour_new, obj_new
            self.obj_tracker.append(self.obj_value)
            self.improvement = improvement


class SimulatedAnnealing(InitialSolution):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.search_iterations = 0

    def search(self, cooling_rate, initial_temp=None):

        if initial_temp:
            initial_temp = initial_temp
        else:
            initial_temp = max(np.mean(self.dist_matrix[0]) * 1.5, 1000)

        np.random.RandomState(seed=0)
        iterations = np.log(initial_temp * (1 - cooling_rate)) / np.log((1 + cooling_rate))
        system_is_cool = initial_temp * (1 - cooling_rate) ** int(self.search_iterations * 0.75)

        temp = initial_temp

        since_best = 0
        best_reset_point = iterations / 10
        best_obj = self.obj_value
        best_tour = self.tour
        self.obj_tracker = []

        while temp > 1:
            i, j = cities_to_swap(self.node_count)

            tour_new = two_opt_swap(self.tour, i, j)
            tour_old = self.tour
            obj_old = self.obj_value
            obj_new = calculate_tour_length(tour_new, self.dist_matrix, self.node_count)

            self.tour, self.obj_value = metropolis(tour_old, tour_new, obj_old, obj_new, temp)
            self.obj_tracker.append(self.obj_value)

            if self.obj_value >= best_obj:
                since_best += 1
            else:
                since_best = 0
                best_obj = self.obj_value
                best_tour = self.tour

            if since_best >= best_reset_point and temp > system_is_cool:
                self.tour = best_tour
                self.obj_value = best_obj

            temp *= 1 - cooling_rate

        self.tour = best_tour
        self.obj_value = best_obj
        self.search_iterations = len(self.obj_tracker)


class IteratedGreedy(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class TabuSearch(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)
