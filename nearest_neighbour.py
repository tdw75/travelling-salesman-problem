from problem_set_up import *
import time


class NearestNeighbour(TspSetUp):
    def __init__(self, input_data):
        TspSetUp.__init__(self, input_data)
        self.tour = []

    def nn_initial_solution(self, starting_node):
        unvisted_nodes = self.nodes
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


if __name__ == "__main__":
    start_time = time.time()

    with open('data\\tsp_493_1', 'r') as input_data_file:
        input_data = input_data_file.read()

    nn = NearestNeighbour(input_data)
    nn.nn_initial_solution(starting_node=0)
    print(nn.tour)
    print(nn.obj_value)
    print("execution time = {:.1f} seconds".format(time.time() - start_time))
