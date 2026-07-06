import time
import pygame
from pygame.locals import *
import random
import itertools
from genetic_algorithm import mutate, order_crossover, generate_random_population, calculate_fitness, sort_population, default_problems
from draw_functions import draw_paths, draw_plot, draw_cities
import sys
import numpy as np
import pygame
from benchmark_att48 import *
from data_loader import load_healthcare_locations


# Define constant values
# pygame
WIDTH, HEIGHT = 800, 400
NODE_RADIUS = 10
FPS = 30
PLOT_X_OFFSET = 450

# GA
N_CITIES = 15
EXPERIMENTS = {
    "Experiment 1": {
        "population": 50,
        "mutation": 0.2
    },
    "Experiment 2": {
        "population": 100,
        "mutation": 0.5
    },
    "Experiment 3": {
        "population": 200,
        "mutation": 0.8
    }
}

CURRENT_EXPERIMENT = "Experiment 2"

POPULATION_SIZE = EXPERIMENTS[CURRENT_EXPERIMENT]["population"]
MUTATION_PROBABILITY = EXPERIMENTS[CURRENT_EXPERIMENT]["mutation"]
N_GENERATIONS = 500

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Initialize problem
# Using Random cities generation



#-----------------------------FIRST MODIFICATION FOR LATER --------------------------

# cities_locations = [(random.randint(NODE_RADIUS + PLOT_X_OFFSET, WIDTH - NODE_RADIUS),
#                      random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS))
#                     for _ in range(N_CITIES)]

#-------------------------------------------------------------------------------------

# Load healthcare dataset
df = load_healthcare_locations()

# Extract GPS coordinates
latitudes = df["latitude"]
longitudes = df["longitude"]

# data normalization for the pygames screen sake in order to be represented properly in the pygame window

# Find minimum and maximum values
min_lat = latitudes.min()
max_lat = latitudes.max()

min_lon = longitudes.min()
max_lon = longitudes.max()

# Convert GPS coordinates into screen coordinates
locations = []

for _, row in df.iterrows():

    x = (
        (row["longitude"] - min_lon)
        / (max_lon - min_lon)
    )

    y = (
        (row["latitude"] - min_lat)
        / (max_lat - min_lat)
    )

    x = int(
        PLOT_X_OFFSET
        + x * (WIDTH - PLOT_X_OFFSET - 20)
    )

    y = int(
        20
        + y * (HEIGHT - 40)
    )

    locations.append({
        "id": row["id"],
        "name": row["name"],
        "type": row["type"],
        "priority": row["priority"],
        "package_weight": row["package_weight"],
        "delivery_type": row["delivery_type"],
        "service_time": row["service_time"],
        "x": x,
        "y": y
    })

cities_locations = [
    (location["x"], location["y"])
    for location in locations
]

location_lookup = {}

for location in locations:
    location_lookup[(location["x"], location["y"])] = location

print(f"Loaded {len(cities_locations)} healthcare locations.")

# # Using Deault Problems: 10, 12 or 15
# WIDTH, HEIGHT = 800, 400
# cities_locations = default_problems[15]


# Using att48 benchmark
# WIDTH, HEIGHT = 1500, 800
# att_cities_locations = np.array(att_48_cities_locations)
# max_x = max(point[0] for point in att_cities_locations)
# max_y = max(point[1] for point in att_cities_locations)
# scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
# scale_y = HEIGHT / max_y
# cities_locations = [(int(point[0] * scale_x + PLOT_X_OFFSET),
#                      int(point[1] * scale_y)) for point in att_cities_locations]
# target_solution = [cities_locations[i-1] for i in att_48_cities_order]
# fitness_target_solution = calculate_fitness(target_solution)
# print(f"Best Solution: {fitness_target_solution}")
# ----- Using att48 benchmark


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSP Solver using Pygame")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1

# Create Initial Population
# TODO:- use some heuristic like Nearest Neighbour our Convex Hull to initialize
population = generate_random_population(cities_locations, POPULATION_SIZE)
best_fitness_values = []
best_solutions = []


# Main game loop
generation = 1
running = True
start_time = time.time()
while running and generation <= N_GENERATIONS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    screen.fill(WHITE)

    population_fitness = [
    calculate_fitness(individual, location_lookup)
    for individual in population
    ]

    population, population_fitness = sort_population(
        population,  population_fitness)

    best_fitness = calculate_fitness(population[0], location_lookup)
    best_solution = population[0]

    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    draw_plot(screen, list(range(len(best_fitness_values))),
              best_fitness_values, y_label="Fitness - Distance (pxls)")

    draw_cities(screen, cities_locations, RED, NODE_RADIUS)
    draw_paths(screen, best_solution, BLUE, width=3)
    draw_paths(screen, population[1], rgb_color=(128, 128, 128), width=1)

    print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)}")

    new_population = [population[0]]  # Keep the best individual: ELITISM

    while len(new_population) < POPULATION_SIZE:

        # selection
        # simple selection based on first 10 best solutions
        # parent1, parent2 = random.choices(population[:10], k=2)

        # solution based on fitness probability
        probability = 1 / np.array(population_fitness)
        parent1, parent2 = random.choices(population, weights=probability, k=2)

        # child1 = order_crossover(parent1, parent2)
        child1 = order_crossover(parent1, parent2)

        child1 = mutate(child1, MUTATION_PROBABILITY)

        new_population.append(child1)

    population = new_population

    pygame.display.flip()
    clock.tick(FPS)

    generation += 1

end_time = time.time()

execution_time = end_time - start_time

print("\n========== EXPERIMENT RESULTS ==========")
print(f"Generations: {N_GENERATIONS}")
print(f"Population Size: {POPULATION_SIZE}")
print(f"Mutation Probability: {MUTATION_PROBABILITY}")
print(f"Best Fitness: {best_fitness:.2f}")
print(f"Execution Time: {execution_time:.2f} seconds")

# TODO: save the best individual in a file if it is better than the one saved.

# exit software
pygame.quit()
sys.exit()
