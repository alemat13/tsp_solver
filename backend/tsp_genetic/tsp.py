import random
from deap import algorithms, base, creator, tools
import numpy as np

def distance(coord1, coord2):
    # Calcul de la distance euclidienne entre deux coordonnées GPS
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    # Conversion des degrés en radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    # Formule de la distance entre deux points sur une sphère
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    # Rayon moyen de la Terre en kilomètres
    R = 6371.0
    distance = R * c
    return distance

def calculate_distances_matrix(coords):
    # Création d'une matrice de distances
    num_points = len(coords)
    distances_matrix = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                distances_matrix[i][j] = distance(coords[i], coords[j])
    return distances_matrix

def evaluate_path(individual, coords, distances_matrix = None):
    # Calcul de la longueur totale du chemin
    total_distance = 0
    for i in range(len(individual) - 1):
        # total_distance += geodesic(coords[individual[i]], coords[individual[i+1]]).meters
        if distances_matrix is not None:
            total_distance += distances_matrix[individual[i]][individual[i+1]]
        else:
            total_distance += distance(coords[individual[i]], coords[individual[i+1]])
    return total_distance,

def solve_tsp_genetic(coords, population_size=100, num_generations=100, distances_matrix=None):
    # Définition du type de problème (minimisation)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Calcul de la matrice de distances
    if distances_matrix is None:
        distances_matrix = calculate_distances_matrix(coords)

    # Initialisation de la boîte à outils
    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(len(coords)), len(coords))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate_path, coords=coords, distances_matrix=distances_matrix)

    # Création de la population initiale
    population = toolbox.population(n=population_size)

    # Algorithme génétique
    algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=num_generations, verbose=True)

    # Sélection de la meilleure solution
    best_individual = tools.selBest(population, k=1)[0]
    # best_path = [coords[i] for i in best_individual]

    return best_individual
