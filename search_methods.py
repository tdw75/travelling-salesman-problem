from initial_solutions import *
from problem_setup import update_tour_length
import random


def cities_to_swap(node_count, nearest_nodes, tour):
    b_idx = np.random.randint(node_count)
    neighbour = random.choice(nearest_nodes[tour[b_idx]])
    d_idx = tour.index(neighbour)
    c_idx = d_idx - 1

    if (b_idx == c_idx) or (b_idx - c_idx) == 1 or (b_idx == 0 and c_idx == node_count - 1):
        b_idx, c_idx = cities_to_swap(node_count, nearest_nodes, tour)

    return b_idx, c_idx


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


def greedy_two_opt(tour, obj, points, node_count, neighbours):
    obj_best = obj
    tour_best = tour

    for node in range(node_count):

        i = tour_best.index(node)

        for neighbour in neighbours[node]:  # vectorise???

            d_idx = tour_best.index(neighbour)
            j = d_idx - 1
            a_idx = i - 1

            a = tour_best[a_idx]
            b = tour_best[i]
            c = tour_best[j]
            d = tour_best[d_idx]
            if a == c:
                continue
            obj_temp = update_tour_length(obj_best, points, nodes=(a, b, c, d))

            if obj_temp < obj_best:
                tour_best = two_opt_swap(tour_best, i, j, node_count)
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

    def search(self, max_iterations=1000):

        if not self.tour:
            raise ValueError("No initial solution has been set")

        tour_new, obj_new = greedy_two_opt(self.tour, self.obj_value, self.coordinates, self.node_count,
                                           self.nearest_nodes)
        improvement = self.obj_value - obj_new
        self.tour, self.obj_value = tour_new, obj_new
        self.obj_tracker.append(self.obj_value)

        self.search_iterations = 0

        while improvement > 0 and self.search_iterations <= max_iterations:
            tour_new, obj_new = greedy_two_opt(self.tour, self.obj_value, self.coordinates, self.node_count,
                                               self.nearest_nodes)
            improvement = self.obj_value - obj_new
            self.tour, self.obj_value = tour_new, obj_new
            self.obj_tracker.append(self.obj_value)
            self.improvement = improvement
            self.search_iterations += 1


class SimulatedAnnealing(InitialSolution):
    def __init__(self, input_data, k=None):
        super().__init__(input_data, k=k)
        self.search_iterations = 0

    def search(self, cooling_rate, initial_temp=None):

        if initial_temp:
            initial_temp = initial_temp
        else:
            initial_temp = max(self.est_mean_edge, 1000)

        np.random.RandomState(seed=0)
        iterations = np.log(initial_temp * (1 - cooling_rate)) / np.log((1 + cooling_rate))
        cooled_system = initial_temp * (1 - cooling_rate) ** int(iterations * 0.9)
        cooling_rate_reduced = False
        reduced_cooling_rate = cooling_rate * 0.25

        temp = initial_temp

        since_best = 0
        best_reset_point = iterations / 10
        best_obj = self.obj_value
        best_tour = self.tour
        self.obj_tracker = []

        while temp > 1:
            i, j = cities_to_swap(self.node_count, self.nearest_nodes, self.tour)

            tour_new = two_opt_swap(self.tour, i, j)
            tour_old = self.tour
            obj_old = self.obj_value

            a_idx = i - 1 if i > 0 else self.node_count - 1
            a = self.tour[a_idx]
            b = self.tour[i]
            c = self.tour[j]
            d_idx = j + 1 if j + 1 < self.node_count else 0
            d = self.tour[d_idx]
            obj_new = update_tour_length(self.obj_value, self.coordinates, nodes=(a, b, c, d))

            self.tour, self.obj_value = metropolis(tour_old, tour_new, obj_old, obj_new, temp)
            self.obj_tracker.append(self.obj_value)

            if self.obj_value >= best_obj:
                since_best += 1
            else:
                since_best = 0
                best_obj = self.obj_value
                best_tour = self.tour

            if since_best >= best_reset_point and temp > cooled_system:
                self.tour = best_tour
                self.obj_value = best_obj

            if temp < cooled_system and not cooling_rate_reduced:
                cooling_rate = reduced_cooling_rate
                cooling_rate_reduced = True

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
