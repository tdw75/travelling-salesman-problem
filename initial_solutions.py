import plotly.graph_objects as go
from problem_setup import *


class NearestNeighbour(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)

    def nn_initial_solution(self, starting_node):
        unvisted_nodes = self.nodes.copy()
        unvisted_nodes.remove(starting_node)
        self.tour = [starting_node]
        self.obj_value = 0
        current_node = starting_node

        while unvisted_nodes:
            closest = min(enumerate(self.dist_matrix[current_node]),
                          key=lambda x: x[1] if (x[1] > 0 and x[0] in unvisted_nodes) else float('inf'))
            self.tour.append(closest[0])
            self.obj_value += closest[1]
            unvisted_nodes.remove(closest[0])
            current_node = closest[0]

        self.obj_value += self.dist_matrix[current_node][starting_node]


class ChristofidesAlgorithm(TspSetUp):
    def __init__(self, input_data):
        super().__init__(input_data)


class InitialSolution(NearestNeighbour):
    def __init__(self, input_data):
        super().__init__(input_data)
        self.obj_tracker = []

    def generate_initial_solution(self, initial_solution):

        initial_solutions = ['nearest neighbour', 'sequential tour', 'random tour']

        if initial_solution not in initial_solutions:
            raise ValueError('Initial solution must be one of \n{}'.format(initial_solutions))

        if initial_solution == "nearest neighbour":
            self.nn_initial_solution(starting_node=np.random.randint(self.node_count))
        elif initial_solution == "sequential tour":
            self.trivial_tour()
        elif initial_solution == 'random tour':
            self.random_tour()

        self.obj_value = calculate_tour_length(self.tour, self.dist_matrix, self.node_count)
        self.obj_tracker.append(self.obj_value)

    def plot_objective_value(self):

        n = len(self.obj_tracker)

        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=np.arange(n), y=self.obj_tracker, name="obj. value",
                                 line_color='midnightblue'))
        fig.update_layout(title_text='Value of the objective function throughout the search process',
                          title_x=0.5,
                          xaxis_title="Iteration",
                          yaxis_title="Objective Value")
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
