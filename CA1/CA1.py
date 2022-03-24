from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
from scipy.spatial import cKDTree
import time

"""
Pathfinding program created by Rikard Radovac and Péter Gaal in the course DAT171
"""


def read_coordinate_file(filename):
    """
    Reads the given file and converts its information to xy-coordinates
    :param filename: The file to convert
    :return: Returns a 2D-Numpy array of coordinates
    """
    with open(filename, "r") as coords:
        a = []
        b = []
        for line in coords:
            components = line.split(",")
            for index in range(2):
                value = float(components[index].strip("{},\n"))
                if index == 0:
                    b.append(math.log(math.tan(math.pi / 4 + (math.pi * value / 360))))
                else:
                    a.append(value * math.pi / 180)
    x_coord = np.array(a)
    y_coord = np.array(b)

    return np.column_stack((x_coord, y_coord))

    # coordinates = []
    # for line in coords:
    # y, x = [float(x) for x in line.replace("{", "").replace("}", "").replace(","," ").rsplit()]
    # x = x*math.pi/180
    # y = math.log(math.tan(math.pi/4 + (math.pi*y/360)))
    # coordinates.append([x, y])


def plot_points(coord_list, indices, graph):
    """
    Plots the points and lines between cities to a graph
    :param coord_list: 2D list of coordinates
    :param indices: 2D list of node pairs
    :param graph: List of shortest nodes to connect.
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for ind, line in enumerate(coord_list):
        plt.plot(line[0], line[1], marker="o", color="r", markersize=0.3)

    # Segments for graph connections to plot
    segments = np.zeros((len(indices), 2, 2))
    for ind, element in enumerate(indices):
        segments[ind, 0, 0] = coord_list[element[0].astype(int)][0]
        segments[ind, 0, 1] = coord_list[element[0].astype(int)][1]
        segments[ind, 1, 0] = coord_list[element[1].astype(int)][0]
        segments[ind, 1, 1] = coord_list[element[1].astype(int)][1]

    # Segments for the shortest path
    fast_seg = np.zeros((1, len(graph), 2))
    for ind, element in enumerate(graph):
        fast_seg[0, ind, 0] = coord_list[element][0]
        fast_seg[0, ind, 1] = coord_list[element][1]

    short_line = LineCollection(fast_seg, linewidths=2.5, color="g")
    line_segments = LineCollection(segments, linewidths=0.4, color="grey")
    ax.add_collection(line_segments)
    ax.add_collection(short_line)
    plt.title("Cities")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.axis("equal")
    plt.show()


def construct_graph_connections(coord_list, radius):
    """
    Constructs all possible city-connections that satisfy the criteria.
    :param coord_list: 2D array of coordinates
    :param radius: The max distance between each point
    :return indices: 2D array of the indices of cities which satisfy the maximum distance
    :return distances: 1D array of the distance between each city-pair
    """
    indices = []
    distances = []
    for ind, coordinate in enumerate(coord_list):
        distance = np.sqrt((coord_list[ind + 1:, 0] - coordinate[0]) ** 2 +  # distances between every city
                           (coord_list[ind + 1:, 1] - coordinate[1]) ** 2)   # without duplicates
        for ind2, value in enumerate(distance):
            if value <= radius:
                indices.append([ind, ind2 + ind + 1])
                distances.append(value)
    return np.array(indices), np.array(distances)


def construct_fast_graph_connections(coord_list, radius):
    """
    Rapidly constructs all possible city-connections that satisfy the criteria using cKDTree
    :param coord_list: 2D array of coordinates
    :param radius: The max distance between each point
    :return indices: 2D array of the indices of cities which satisfy the maximum distance
    :return distances: 1D array of the distances between each city-pair
    """
    tree = cKDTree(coord_list)
    indices = []
    distances = []
    nearby_indices = tree.query_ball_point(coord_list, radius)
    for ind, value in enumerate(nearby_indices):
        for ind2 in value:
            if ind < ind2:
                indices.append([ind, ind2])
                distances.append(math.dist(coord_list[ind], coord_list[ind2]))
    return np.array(indices), np.array(distances)


def construct_graph(indices, distances, N):
    """
    Constructs a graph (compressed sparse row matrix) of paired cities.
    :param indices: 2D array of indices of cities which satisfy the maximum distance
    :param distances: 1D array of the distances between each city pair
    :param N: Total number of pairs in indices
    :return graph: Compressed sparse row matrix of the indices combined with distances
    """

    graph = (csr_matrix((distances, (indices[:, 0], indices[:, 1])), shape=(N, N)))
    return graph


def find_shortest_path(graph, start_node, end_node):
    """
    Finds the shortest path between two nodes in a constructed graph
    :param graph: Compressed sparse row matrix of the indices combined with distances
    :param start_node: The city to find the shortest path from
    :param end_node: The city to find the shortest path to
    :return path: The shortest path city-sequence
    :return path[::-1]: the shortest path city-sequence in order from start to end
    :return dist_matrix[0, end_node]: The total distance between start and end
    """
    dist_matrix, predecessor = shortest_path(csgraph=graph, directed=False, indices=start_node,
                                             return_predecessors=True)
    print(f"The distance between start and end: {dist_matrix[end_node]}")

    path = [end_node]  # list of cities starting from the end
    while predecessor[end_node] > -9999:
        path.append(predecessor[end_node])  # Appending the previously visited city
        end_node = predecessor[end_node]
    print(f"The sequence of cities: {path[::-1]}")
    return path[::-1], dist_matrix[end_node]


def main():
    """
    The main function which executes the program in the correct order and prints the output
    to a text document.
    """

    choices = {
        "Country": ["Sample", "Hungary", "Germany"],
        "Radius": [0.08, 0.005, 0.0025],
        "Start node": [0, 311, 1573],
        "End node": [5, 702, 10584],
        "Filepath": ["SampleCoordinates.txt", "HungaryCities.txt",
                     "GermanyCities.txt"]
    }

    while True:
        choice = input("Choose city, S for sample, H for Hungary, G for Germany \n")
        if choice == "S" or choice == "s":
            country = choices["Country"][0]
            radius = choices["Radius"][0]
            start_node = choices["Start node"][0]
            end_node = choices["End node"][0]
            file = choices["Filepath"][0]
            break

        if choice == "H" or choice == "h":
            country = choices["Country"][1]
            radius = choices["Radius"][1]
            start_node = choices["Start node"][1]
            end_node = choices["End node"][1]
            file = choices["Filepath"][1]
            break

        if choice == "G" or choice == "g":
            country = choices["Country"][2]
            radius = choices["Radius"][2]
            start_node = choices["Start node"][2]
            end_node = choices["End node"][2]
            file = choices["Filepath"][2]
            break
        else:
            print("Please retype your choice")
            continue

    while True:
        choice = input("FAST for for fast connections, SLOW for slow (no use of cKDTree) \n")
        if choice == "FAST" or choice == "fast":
            chosen_function = construct_fast_graph_connections
            break
        elif choice == "SLOW" or choice == "slow":
            chosen_function = construct_graph_connections
            break
        else:
            print("Please retype your choice")
            continue

    with open("Output.txt", "w") as output:
        output.write(f"Country: {country}\n")

    start_time = time.time()
    coordinates = read_coordinate_file(file)
    with open("Output.txt", "a") as output:
        output.write(f"reading file time: {time.time() - start_time} \n")

    start_time = time.time()
    indices, distances = chosen_function(coordinates, radius)
    with open("Output.txt", "a") as output:
        output.write(f"construct graph connections time: {time.time() - start_time} \n")

    start_time = time.time()
    constructed_graph = construct_graph(indices, distances, len(coordinates))
    with open("Output.txt", "a") as output:
        output.write(f"construct graph time: {time.time() - start_time} \n")

    start_time = time.time()
    city_sequence, total_distance = find_shortest_path(constructed_graph, start_node, end_node)
    with open("Output.txt", "a") as output:
        output.write(f"shortest path time: {time.time() - start_time} \n")

    start_time = time.time()
    plot_points(coordinates, indices, city_sequence)
    with open("Output.txt", "a") as output:
        output.write(f"plot points time: {time.time() - start_time} \n \n")

    with open("Output.txt", "a") as output:
        output.write(f"The total sequence of cities is {city_sequence}\n")
        output.write(f"The total distance between start and end is {total_distance}")


if __name__ == "__main__":
    main()
