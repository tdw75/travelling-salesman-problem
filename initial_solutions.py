import plotly.graph_objects as go
from problem_setup import *
import random


class NearestNeighbour(TspSetUp):
    def __init__(self, input_data, k=None):
        super().__init__(input_data, k=k)

    def nn_initial_solution(self, starting_node):
        unvisited_nodes = self.nodes.copy()
        unvisited_nodes.remove(starting_node)
        self.tour = [starting_node]
        self.obj_value = 0
        current_node = starting_node

        while unvisited_nodes:
            closest = [x for x in self.nearest_nodes[current_node] if x in unvisited_nodes]
            if closest:
                next_node = closest[0]
            else:
                next_node = random.choice(unvisited_nodes)

            self.tour.append(next_node)
            unvisited_nodes.remove(next_node)
            current_node = next_node

        self.obj_value = calculate_tour_length(self.tour, self.coordinates, self.node_count)


class ChristofidesAlgorithm(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class InitialSolution(NearestNeighbour):
    def __init__(self, input_data, k=None):
        super().__init__(input_data, k=k)
        self.obj_tracker = []

    def generate_initial_solution(self, initial_solution=None):

        initial_solutions = ['nearest neighbour', 'sequential tour', 'random tour']

        if initial_solution:

            if initial_solution not in initial_solutions:
                raise ValueError('Initial solution must be one of \n{}'.format(initial_solutions))

            if initial_solution == "nearest neighbour":
                self.nn_initial_solution(starting_node=36)
            elif initial_solution == "sequential tour":
                self.trivial_tour()
            elif initial_solution == 'random tour':
                self.random_tour()
        else:
            if self.node_count < 2000:
                self.nn_initial_solution(starting_node=36)
            else:
                self.trivial_tour()

        if self.obj_value:
            pass
        else:
            self.obj_value = calculate_tour_length(self.tour, self.coordinates, self.node_count)
        self.obj_tracker.append(self.obj_value)

    def plot_objective_value(self):

        n = len(self.obj_tracker)
        step = int(n/1000000) + 1

        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=np.arange(0, n, step), y=self.obj_tracker[::step], name="obj. value",
                                   line_color='midnightblue'))
        fig.update_layout(title_text='Value of the objective function throughout the search process',
                          title_x=0.5,
                          xaxis_title="Iteration",
                          yaxis_title="Objective Value")
        fig.update_yaxes(range=[0, np.max(self.obj_tracker) * 1.1])

        fig.show()


if __name__ == "__main__":
    import time

    with open('data\\tsp_51_1', 'r') as input_data_file:
        input_data = input_data_file.read()

    start_time = time.time()
    nn = NearestNeighbour(input_data)
    nn.nn_initial_solution(starting_node=44)
    print(nn.tour)
    print(nn.obj_value)
    nn.plot_tour()
    print("execution time = {:.1f} seconds".format(time.time() - start_time))
