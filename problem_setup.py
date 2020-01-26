import math
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


def euclidean_distance(point1, point2):
    dist = [(a - b) ** 2 for a, b in zip(point1, point2)]
    dist = math.sqrt(sum(dist))
    return dist


def distance_matrix(points):
    dist_matrix = {}

    for node, point in enumerate(points):
        dist = cdist(points, np.array([point]))
        dist_matrix[node] = np.array([x[0] for x in dist])

    return dist_matrix


def nearest_k_nodes(points, dist_matrix: dict = None, k=25):
    if not dist_matrix:

        dist_matrix = {}

        for node, point in enumerate(points):
            dist = cdist(points, np.array([point]))
            dist_matrix[node] = np.array([x[0] for x in dist])

    nearest_k = {}

    for node in dist_matrix:
        nearest_k[node] = dist_matrix[node].argsort()[1:k + 1]

    return nearest_k


def parse_input_data(input_data):
    lines = input_data.split('\n')

    node_count = int(lines[0])
    nodes = list(range(node_count))
    points = []

    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))

    return points, node_count, nodes


def calculate_tour_length(tour, points, node_count):
    if not node_count:
        node_count = len(tour)

    obj = euclidean_distance(points[tour[-1]], points[tour[0]])
    for idx in range(0, node_count - 1):
        obj += euclidean_distance(points[tour[idx]], points[tour[idx + 1]])

    return obj


def update_tour_length(obj_val, points, nodes: tuple):
    a = points[nodes[0]]
    b = points[nodes[1]]
    c = points[nodes[2]]
    d = points[nodes[3]]

    new_obj = obj_val - euclidean_distance(a, b) - euclidean_distance(c, d) \
              + euclidean_distance(a, c) + euclidean_distance(b, d)

    return new_obj


def select_k(node_count):
    if node_count <= 250:
        return 10
    elif node_count <= 2500:
        return 25
    else:
        return 25


class TspSetUp:
    def __init__(self, input_data, k=None):
        self.coordinates, self.node_count, self.nodes = parse_input_data(input_data)
        self.dist_matrix = distance_matrix(self.coordinates)

        if not k:
            k = select_k(self.node_count)

        self.nearest_nodes = nearest_k_nodes(self.coordinates, self.dist_matrix, k=k)
        self.est_mean_edge = np.mean(self.dist_matrix[0]) * 1.5
        del self.dist_matrix

        self.tour = []
        self.obj_value = None
        self.edges = None

    def random_tour(self):

        length = self.node_count
        for x in self.nodes:
            next_node = np.random.randint(length)
            self.tour.append(next_node)
            length -= 1

        self.obj_value = calculate_tour_length(self.tour, self.coordinates, self.node_count)

    def trivial_tour(self):
        self.tour = list(range(0, self.node_count))
        self.obj_value = calculate_tour_length(self.tour, self.coordinates, self.node_count)

    def save_solution(self):
        pass

    def plot_tour(self):

        fig, ax = plt.subplots(figsize=(12, 8))

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
