import math
from collections import namedtuple
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


def euclidean_distance1(point1, point2):
    return 5
    #return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def euclidean_distance(point1, point2):
    dist = [(a - b) ** 2 for a, b in zip(point1, point2)]
    dist = math.sqrt(sum(dist))
    return dist


def distance_matrix(points):
    distances = {}

    for node, point in enumerate(points):
        dist = cdist(points, np.array([point]))
        distances[node] = np.array([x[0] for x in dist])
        # distances.append(np.array([x[0] for x in dist]))

    # distances = np.array(distances)

    return distances


def parse_input_data(input_data):
    # Point = namedtuple("Point", ['x', 'y'])
    lines = input_data.split('\n')

    node_count = int(lines[0])
    nodes = list(range(node_count))
    points = []

    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))  # normal tuple
        # points.append(Point(float(parts[0]), float(parts[1]))) # named tuple

    return points, node_count, nodes


def calculate_tour_length(tour, dist_matrix, node_count):
    obj_val = dist_matrix[tour[-1]][tour[0]]

    for idx in range(0, node_count - 1):
        obj_val += dist_matrix[tour[idx]][tour[idx + 1]]

    return obj_val


class TspSetUp:
    def __init__(self, input_data):
        self.coordinates, self.node_count, self.nodes = parse_input_data(input_data)
        self.dist_matrix = distance_matrix(self.coordinates)
        self.tour = []
        self.obj_value = None
        self.edges = None

    def random_tour(self):

        length = self.node_count
        for x in self.nodes:
            next_node = np.random.randint(length)
            self.tour.append(next_node)
            length -= 1

        self.obj_value = calculate_tour_length(self.tour, self.dist_matrix, self.node_count)

    def trivial_tour(self):
        self.tour = list(range(0, self.node_count))
        self.obj_value = calculate_tour_length(self.tour, self.dist_matrix, self.node_count)

    def save_solution(self):
        pass

    def plot_tour(self):

        fig, ax = plt.subplots(figsize=(15, 10))

        graph = nx.Graph()
        graph.add_nodes_from(self.nodes)

        for i in range(self.node_count - 1):
            graph.add_edge(self.tour[i], self.tour[i + 1])

        graph.add_edge(self.tour[-1], self.tour[0])
        positions = dict((node, position) for node, position in enumerate(self.coordinates))

        nx.draw(graph, positions, with_labels=True)
        plt.show()

    def generate_edges(self):
        self.edges = []
        self.edges.append((self.tour[-1], self.tour[0]))

        for i in range(self.node_count - 1):
            self.edges.append((self.tour[i], self.tour[i + 1]))


if __name__ == "__main__":
    with open('data\\tsp_1000_1', 'r') as input_data_file:
        input_data = input_data_file.read()

    start_time = time.time()
    tsp = TspSetUp(input_data)
    tsp.random_tour()
    print(tsp.tour)
    print("execution time = {:.1f} seconds".format(time.time() - start_time))
