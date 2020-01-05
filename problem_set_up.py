import math
from collections import namedtuple
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt


def euclidean_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def distance_matrix(points):
    distances = {}
    for node, point1 in enumerate(points):

        distances[node] = []

        for point2 in points:
            distance = euclidean_distance(point1, point2)
            distances[node].append(distance)

    return distances


def parse_input_data(input_data):
    Point = namedtuple("Point", ['x', 'y'])
    lines = input_data.split('\n')

    node_count = int(lines[0])
    nodes = list(range(node_count))
    points = []

    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    return points, node_count, nodes


class TspSetUp:
    def __init__(self, input_data):
        self.coordinates, self.node_count, self.nodes = parse_input_data(input_data)
        self.dist_matrix = distance_matrix(self.coordinates)
        self.tour = []
        self.obj_value = None
        self.edges = None

    def calculate_tour_length(self):
        self.obj_value = euclidean_distance(self.coordinates[self.tour[-1]], self.coordinates[self.tour[0]])

        for idx in range(0, self.node_count - 1):
            self.obj_value += euclidean_distance(self.coordinates[self.tour[idx]], self.coordinates[self.tour[idx + 1]])

    def random_tour(self):

        length = self.node_count
        for x in self.nodes:
            next_node = np.random.randint(length)
            self.tour.append(next_node)
            length -= 1

        self.calculate_tour_length()

    def trivial_tour(self):
        self.tour = range(0, self.node_count)
        self.calculate_tour_length()

    def save_solution(self):
        pass

    def plot_tour(self):
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
