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

def calculate_route(positions):

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

    dm = OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=True)

    # Afficher le résultat à l'utilisateur
    distances_matrix = dm.get_distances_matrix(positions)

    optimal_route = get_optimal_route(
        positions, distances_matrix=distances_matrix)
    app.logger.debug(optimal_route)

    route = dm.get_route(optimal_route)
    geometry = route['features'][0]['geometry']['coordinates']
    latLng = [[lng, lat] for lat, lng in geometry]

    return {'optimal_route': optimal_route, 'route': latLng}


if __name__ == '__main__':
    positions = [
        [48.8606, 2.3376],
        [48.853, 2.3499],
        [48.8738, 2.295],
        [48.8867, 2.3431],
        [48.86, 2.3267],
        [48.8698, 2.3075],
        [48.8635, 2.3274],
        [48.8462, 2.3447],
        [48.8656, 2.3212],
        [48.8556, 2.3158]
    ]
    # todo : write test for positions
    app.run(debug=True, host='0.0.0.0')
