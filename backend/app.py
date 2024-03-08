from flask import Flask, request, send_from_directory
from flask_cors import CORS
from openrouteservice import OpenRouteService
import configparser

REACT_BUILD_DIR = '../frontend/build'

app = Flask(__name__, static_folder=REACT_BUILD_DIR, static_url_path='/')
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

    sslVerify = config['ssl']['verify']

    return OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=(sslVerify.lower == 'true'))

def calculate_route(positions):
    ors = get_open_route_service()

    # Afficher le résultat à l'utilisateur
    distances_matrix = ors.get_distances_matrix(positions)

    optimal_route = get_optimal_route(
        positions, distances_matrix=distances_matrix)

    geometry = ors.get_geometry(optimal_route)

    return {'optimal_route': optimal_route, 'route': geometry, 'distances_matrix': distances_matrix}

@app.route('/api/calculate', methods=['POST', 'GET'])
def calculate_route_api():
    positions = request.json
    return calculate_route(positions)

@app.route('/static/<path:path>')
def serve_static(path):
    print('serve_static', path)
    return send_from_directory(f'{REACT_BUILD_DIR}/static', path)
@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def serve(path):
    print('serve', path)
    if path != "" and path != "favicon.ico":
        return send_from_directory(f'{REACT_BUILD_DIR}', path)
    else:
        return send_from_directory(f'{REACT_BUILD_DIR}', 'index.html')

if __name__ == '__main__':
    
    # todo : write test for positions
    app.run(debug=True, host='0.0.0.0')
