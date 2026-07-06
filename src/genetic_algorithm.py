import random
import math
import copy 
from typing import List, Tuple

default_problems = {
5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
10:[(470, 169), (602, 202), (754, 239), (476, 233), (468, 301), (522, 29), (597, 171), (487, 325), (746, 232), (558, 136)],
12:[(728, 67), (560, 160), (602, 312), (712, 148), (535, 340), (720, 354), (568, 300), (629, 260), (539, 46), (634, 343), (491, 135), (768, 161)],
15:[(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)]
}

def generate_random_population(cities_location: List[Tuple[float, float]], population_size: int) -> List[List[Tuple[float, float]]]:
    """
    Generate a random population of routes for a given set of cities.

    Parameters:
    - cities_location (List[Tuple[float, float]]): A list of tuples representing the locations of cities,
      where each tuple contains the latitude and longitude.
    - population_size (int): The size of the population, i.e., the number of routes to generate.

    Returns:
    List[List[Tuple[float, float]]]: A list of routes, where each route is represented as a list of city locations.
    """
    return [random.sample(cities_location, len(cities_location)) for _ in range(population_size)]

def calculate_route_distance(path, location_lookup):

    distance = 0

    n = len(path)

    for i in range(n):

        current = location_lookup[path[i]]

        nxt = location_lookup[path[(i + 1) % n]]

        distance += calculate_distance(

            (current["x"], current["y"]),

            (nxt["x"], nxt["y"])

        )

    return distance

def calculate_priority_penalty(path, location_lookup):

    penalty = 0

    for position, point in enumerate(path):

        location = location_lookup[point]

        if location["priority"] == 3:
            penalty += position * 5

        elif location["priority"] == 2:
            penalty += position * 3

        else:
            penalty += position

    return penalty

def calculate_capacity_penalty(path, location_lookup):

    vehicle_capacity = 20

    total_weight = 0

    for point in path:

        location = location_lookup[point]

        total_weight += location["package_weight"]

    if total_weight > vehicle_capacity:

        return (total_weight - vehicle_capacity) * 50

    return 0

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate the Euclidean distance between two points.

    Parameters:
    - point1 (Tuple[float, float]): The coordinates of the first point.
    - point2 (Tuple[float, float]): The coordinates of the second point.

    Returns:
    float: The Euclidean distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def calculate_distance_penalty(path, location_lookup):
    
    max_route_distance = 6000

    route_distance = calculate_route_distance(
        path,
        location_lookup
    )

    if route_distance > max_route_distance:

        excess = route_distance - max_route_distance

        return excess * 2

    return 0

def calculate_fitness(path: List[Tuple[float, float]], location_lookup: dict) -> float:
    """
    Calculate the total fitness of a route.
    Lower values represent better routes.
    """

    distance = calculate_route_distance(path, location_lookup)

    priority_penalty = calculate_priority_penalty(
        path,
        location_lookup
    )

    capacity_penalty = calculate_capacity_penalty(
        path,
        location_lookup
    )

    distance_penalty = calculate_distance_penalty(
        path,
        location_lookup
    )

    return (
        distance
        + priority_penalty
        + capacity_penalty
        + distance_penalty
    )


def order_crossover(parent1, parent2):

    size = len(parent1)

    child = [None] * size

    start, end = sorted(random.sample(range(size), 2))

    # Copy slice from parent1
    child[start:end] = parent1[start:end]

    # Fill remaining positions from parent2
    p2_index = 0

    for i in range(size):

        if child[i] is None:

            while parent2[p2_index] in child:
                p2_index += 1

            child[i] = parent2[p2_index]

            p2_index += 1

    return child

### demonstration: crossover test code
# Example usage:
# parent1 = [(1, 1), (2, 2), (3, 3), (4,4), (5,5), (6, 6)]
# parent2 = [(6, 6), (5, 5), (4, 4), (3, 3),  (2, 2), (1, 1)]

# # parent1 = [1, 2, 3, 4, 5, 6]
# # parent2 = [6, 5, 4, 3, 2, 1]


# child = order_crossover(parent1, parent2)
# print("Parent 1:", [0, 1, 2, 3, 4, 5, 6, 7, 8])
# print("Parent 1:", parent1)
# print("Parent 2:", parent2)
# print("Child   :", child)


# # Example usage:
# population = generate_random_population(5, 10)

# print(calculate_fitness(population[0]))


# population = [(random.randint(0, 100), random.randint(0, 100))
#           for _ in range(3)]

def tournament_selection(population, fitness, tournament_size=5):
    """
    Select one parent using tournament selection.
    """

    contestants = random.sample(
        list(zip(population, fitness)),
        tournament_size
    )

    contestants.sort(key=lambda x: x[1])

    return contestants[0][0]

# TODO: implement a mutation_intensity and invert pieces of code instead of just swamping two. 
def mutate(solution:  List[Tuple[float, float]], mutation_probability: float) ->  List[Tuple[float, float]]:
    """
    Mutate a solution by inverting a segment of the sequence with a given mutation probability.

    Parameters:
    - solution (List[int]): The solution sequence to be mutated.
    - mutation_probability (float): The probability of mutation for each individual in the solution.

    Returns:
    List[int]: The mutated solution sequence.
    """
    mutated_solution = copy.deepcopy(solution)

    # Check if mutation should occur    
    if random.random() < mutation_probability:
        
        # Ensure there are at least two cities to perform a swap
        if len(solution) < 2:
            return solution
    
    index1 = random.randint(0, len(solution) - 1)
    index2 = random.randint(0, len(solution) - 1)

    while index1 == index2:
        index2 = random.randint(0, len(solution) - 1)

    mutated_solution[index1], mutated_solution[index2] = (
        mutated_solution[index2],
        mutated_solution[index1]
    )
            
    return mutated_solution

### Demonstration: mutation test code    
# # Example usage:
# original_solution = [(1, 1), (2, 2), (3, 3), (4, 4)]
# mutation_probability = 1

# mutated_solution = mutate(original_solution, mutation_probability)
# print("Original Solution:", original_solution)
# print("Mutated Solution:", mutated_solution)


def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    """
    Sort a population based on fitness values.

    Parameters:
    - population (List[List[Tuple[float, float]]]): The population of solutions, where each solution is represented as a list.
    - fitness (List[float]): The corresponding fitness values for each solution in the population.

    Returns:
    Tuple[List[List[Tuple[float, float]]], List[float]]: A tuple containing the sorted population and corresponding sorted fitness values.
    """
    # Combine lists into pairs
    combined_lists = list(zip(population, fitness))

    # Sort based on the values of the fitness list
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])

    # Separate the sorted pairs back into individual lists
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return sorted_population, sorted_fitness


if __name__ == '__main__':
    N_CITIES = 10
    
    POPULATION_SIZE = 100
    N_GENERATIONS = 100
    MUTATION_PROBABILITY = 0.3
    cities_locations = [(random.randint(0, 100), random.randint(0, 100))
              for _ in range(N_CITIES)]
    
    # CREATE INITIAL POPULATION
    population = generate_random_population(cities_locations, POPULATION_SIZE)

    # Lists to store best fitness and generation for plotting
    best_fitness_values = []
    best_solutions = []
    
    for generation in range(N_GENERATIONS):
  
        
        population_fitness = [calculate_fitness(individual) for individual in population]    
        
        population, population_fitness = sort_population(population,  population_fitness)
        
        best_fitness = calculate_fitness(population[0])
        best_solution = population[0]
           
        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)    

        print(f"Generation {generation}: Best fitness = {best_fitness}")

        new_population = [population[0]]  # Keep the best individual: ELITISM
        
        while len(new_population) < POPULATION_SIZE:
            
            # SELECTION
            parent1, parent2 = random.choices(population[:10], k=2)  # Select parents from the top 10 individuals
            
            # CROSSOVER
            child1 = order_crossover(parent1, parent2)
            
            ## MUTATION
            child1 = mutate(child1, MUTATION_PROBABILITY)
            
            new_population.append(child1)
            
    
        print('generation: ', generation)
        population = new_population
    


