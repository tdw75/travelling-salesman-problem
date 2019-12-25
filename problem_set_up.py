import math
from collections import namedtuple


def euclidean_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def distance_matrix(points):
    distances = {}
    node = 0
    for point1 in points:

        distances[node] = []

        for point2 in points:
            distance = euclidean_distance(point1, point2)
            distances[node].append(distance)

        node += 1

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
        self.obj_value = None

    def calculate_tour_length(self):
        pass

    def save_solution(self):
        pass

    def plot_tour(self):
        pass


if __name__ == "__main__":
    with open('data\\tsp_5_1', 'r') as input_data_file:
        input_data = input_data_file.read()

    tsp = TspSetUp(input_data)
    print(tsp.coordinates)
    print(tsp.dist_matrix.keys())
