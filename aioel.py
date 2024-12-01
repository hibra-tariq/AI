import random
import math

# Define a set of cities as (x, y) coordinates
CITIES = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1

# Calculate Euclidean distance between two cities


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# Calculate the total distance of a route


def route_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1)) + distance(route[-1], route[0])


# Fitness function: inverse of route distance (shorter route = higher fitness)


def fitness(route):
    return 1 / route_distance(route)

# Create a random route


def create_route():
    route = CITIES[:]
    random.shuffle(route)
    return route

# Generate the initial population


def create_population():
    return [create_route() for _ in range(POPULATION_SIZE)]

# Tournament selection


def select_parent(population):
    tournament = random.sample(population, 5)
    return max(tournament, key=fitness)

# Ordered crossover


def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)

    # Inherit a slice from parent1
    child[start:end] = parent1[start:end]

    # Fill in the remaining cities from parent2 in order
    ptr = 0
    for city in parent2:
        if city not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = city

    return child

# Swap mutation


def mutate(route):
    for i in range(len(route)):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]

# Main genetic algorithm function


def genetic_algorithm():
    population = create_population()

    for generation in range(GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        best_route = population[0]
        print(f"Generation {generation}, Best Distance: {round(route_distance(best_route),3)} km")

        # Create the next generation
        next_generation = population[:2]  # Elitism: carry forward the best 2 routes

        while len(next_generation) < POPULATION_SIZE:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation

    # Print final results
    best_route = min(population, key=route_distance)
    print("Best route:", best_route)
    print("Best distance:", round(route_distance(best_route), 3), "km")

# Run the genetic algorithm

genetic_algorithm()
