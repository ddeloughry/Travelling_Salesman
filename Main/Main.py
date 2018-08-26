import math
import os
import random

import matplotlib.pyplot as efficiency_graph
import matplotlib.pyplot as tsp_map


def get_coordinates(coordinates_file):
    """
    Get coordinates from file
    :param coordinates_file:
    :return: coordinates: List of coordinates
    """
    coordinates = list()
    for each_line in coordinates_file:
        current = list()
        current.append(int(each_line.split()[0]))
        current.append(int(each_line.split()[1]))
        coordinates.append(current)
    return coordinates


def do_simulated_annealing(coordinates, distances_list, current_solution, starting_efficiency):
    """
    Perform simulated annealing algorithm
    :param
        coordinates:
        distances_list:
        current_solution:
        starting_efficiency
    :return:
        best_solution:
        efficiency_list:
        best_efficiency:
    """
    temperature = math.sqrt(len(coordinates))
    current_efficiency = starting_efficiency
    best_efficiency = starting_efficiency
    efficiency_list = [starting_efficiency]
    best_solution = list(current_solution)
    i = 0
    while temperature > 0 and i < 100000:
        candidate = list(current_solution)
        num_a = random.randint(2, len(coordinates) - 1)
        num_b = random.randint(0, len(coordinates) - num_a)
        candidate[num_b:(num_b + num_a)] = reversed(candidate[num_b:(num_b + num_a)])
        candidate_efficiency = get_efficiency(candidate, distances_list, len(coordinates))
        if candidate_efficiency < current_efficiency:
            current_efficiency = candidate_efficiency
            current_solution = candidate
            if candidate_efficiency < best_efficiency:
                best_efficiency = candidate_efficiency
                best_solution = candidate
        else:
            if random.random() < get_probability(candidate_efficiency, current_efficiency, temperature):
                current_efficiency = candidate_efficiency
                current_solution = candidate
        temperature *= 0.995
        i += 1
        efficiency_list.append(current_efficiency)
    return best_solution, efficiency_list, best_efficiency


def get_distances_list(coordinates):
    """
    Get nested lists of distances between all points
    :param coordinates:
    :return: all_distances:
    """
    all_distances = list()
    for i in coordinates:
        distances_from_i = list()
        for j in coordinates:
            i_to_j = round(math.sqrt(math.pow(i[0] - j[0], 2) + math.pow(i[1] - j[1], 2)), 4)
            distances_from_i.append(i_to_j)
        all_distances.append(distances_from_i)
    return all_distances


def get_efficiency(solution, distances_list, num_coordinates):
    """
    Get efficiency of a solution
    :param
        solution:
        distances_list:
        num_coordinates:
    :return: efficiency:
    """
    efficiency = 0
    for i in range(num_coordinates):
        if i > 0:
            efficiency += distances_list[solution[i - 1]][solution[i]]
    efficiency += distances_list[solution[0]][solution[num_coordinates - 1]]
    efficiency = round(efficiency, 4)
    return efficiency


def get_initial_solution(dist_matrix, coordinates):
    """
    Get initial solution using greedy algorithm
    :param
        dist_matrix:
        coordinates:
    :return: solution:
    """
    current_node = random.randint(0, len(coordinates))
    solution = [current_node]
    temp_list = list(list(range(0, len(coordinates))))
    temp_list.remove(current_node)
    for _ in range(len(temp_list)):
        distances = list()
        for i in temp_list:
            distances.append(dist_matrix[current_node][i])
        current_node = dist_matrix[current_node].index(min(distances))
        temp_list.remove(current_node)
        solution.append(current_node)
    return solution


def get_probability(candidate_efficiency, current_efficiency, temperature):
    """
    Get probability of accepting based on candidate and current efficiency and temperature
    :param
        candidate_efficiency:
        current_efficiency:
        temperature:
    :return: probability:
    """
    probability = math.exp(-abs(candidate_efficiency - current_efficiency) / temperature)
    return probability


def get_efficiency_improvement(initial_efficiency, best_efficiency):
    """
    Get improvement of "best_efficiency" over "initial_efficiency"
    :param
        initial_efficiency:
        best_efficiency:
    :return: improvement:
    """
    improvement = round((initial_efficiency - best_efficiency) / initial_efficiency, 4)
    return improvement


def draw_graphs(best_solution, efficiency_list, coordinates):
    """
    Draw TSP diagram and graph of efficiencies
    :param
        coordinates:
        best_solution:
        efficiency_list:
    """
    # Draw efficiency graph
    efficiency_graph.plot(efficiency_list)
    efficiency_graph.ylabel("Efficiency")
    efficiency_graph.xlabel("Iteration")
    efficiency_graph.show()
    # Draw map of tsp route
    xs = list()
    ys = list()
    for i in [best_solution][0]:
        xs.append(coordinates[i][0])
        ys.append(coordinates[i][1])
    tsp_map.plot(xs, ys, "co")
    tsp_map.arrow(xs[-1], ys[-1], (xs[0] - xs[-1]), (ys[0] - ys[-1]))
    for i in range(0, len(xs) - 1):
        tsp_map.arrow(xs[i], ys[i], (xs[i + 1] - xs[i]), (ys[i + 1] - ys[i]))
    tsp_map.show()


def print_results(algorithm_type, best_efficiency, improvement):
    """
    Print algorithm type and results
    :param
        algorithm_type:
        best_efficiency:
        improvement:
    """
    print(algorithm_type + ":\nOptimum efficiency: " + str(
        best_efficiency) + "\nImprovement: " + str(improvement))


def my_main(data_file_name):
    """
    Main function where the above functions are called from
    :param data_file_name:
    """
    # Get city coordinates
    coordinates_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, data_file_name)))
    coordinates = get_coordinates(coordinates_file)
    # Get distances
    distances_list = get_distances_list(coordinates)
    # Get initial solution
    current_solution = get_initial_solution(distances_list, coordinates)
    # Get starting efficiency
    starting_efficiency = get_efficiency(current_solution, distances_list, len(coordinates))
    # Simulated Annealing
    print("-------------------")
    sa_best_solution, sa_efficiency_list, sa_best_efficiency = do_simulated_annealing(coordinates,
                                                                                      distances_list,
                                                                                      current_solution,
                                                                                      starting_efficiency)
    print_results("Simulated Annealing", sa_best_efficiency,
                  get_efficiency_improvement(starting_efficiency, sa_best_efficiency))
    draw_graphs(sa_best_solution, sa_efficiency_list, coordinates)


if __name__ == "__main__":
    # # For testing with 15 cities
    # file_name = "Cities/15City.txt"

    # For testing with 48 cities
    file_name = "Cities/50City.txt"

    my_main(file_name)
