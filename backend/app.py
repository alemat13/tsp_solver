import sys
from flask import Flask, Response, render_template, request
from flask_cors import CORS
from openrouteservice import OpenRouteService
import configparser

app = Flask(__name__)
CORS(app)


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_solver_tour_genetic(points, population_size=100, num_generations=100, distances_matrix=None):
    from tsp_genetic import solve_tsp_genetic
    return solve_tsp_genetic(points, population_size, num_generations, distances_matrix)


def get_optimal_route(points, distances_matrix=None):
    # Calculer le chemin optimal avec Concorde
    try:
        from app_utils import get_solver_tour_concorde
        tour_indices = get_solver_tour_concorde(
            points, distances_matrix=distances_matrix)
    except ImportError:
        tour_indices = get_solver_tour_genetic(
            points, population_size=1000, num_generations=300, distances_matrix=distances_matrix)

    # Renvoyer les positions dans l'ordre du chemin optimal
    return [points[i] for i in tour_indices]


@app.route('/api/calculate', methods=['POST', 'GET'])
def calculate_route_api():
    positions = request.json
    return calculate_route(positions)

def get_open_route_service():
    config = get_config()

    # Check if config['proxies'] is defined
    if 'proxies' in config:
        proxies = {
            "http": config['proxies']['http'],
            "https": config['proxies']['https'],
        }
    else:
        proxies = None

    api_key = config['api_keys']['openrouteservice_api_key']

    return OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=True)

def calculate_route(positions):
    ors = get_open_route_service()

    # Afficher le résultat à l'utilisateur
    distances_matrix = ors.get_distances_matrix(positions)
    
    # transform float to int
    distances_matrix = [[int(j) for j in i] for i in distances_matrix]
    print(distances_matrix)

    optimal_route = get_optimal_route(
        positions, distances_matrix=distances_matrix)

    geometry = ors.get_geometry(optimal_route)

    return {'optimal_route': optimal_route, 'route': geometry, 'distances_matrix': distances_matrix}


if __name__ == '__main__':
    
    # todo : write test for positions
    app.run(debug=True, host='0.0.0.0')
