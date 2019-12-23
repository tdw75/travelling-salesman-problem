import math
from collections import namedtuple


def euclidean_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def parse_input_data(input_data):
    Point = namedtuple("Point", ['x', 'y'])
    lines = input_data.split('\n')

    node_count = int(lines[0])
    points = []

    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    return points


def distance_matrix(points):
    distances = {}
    for point1 in points:
        distances[point1] = []

        for point2 in points:
            distance = euclidean_distance(point1, point2)
            distances[point1].append(distance)

    return distances


def calculate_tour_length():
    pass