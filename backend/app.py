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



def get_open_route_service(api_key=None):
    config = get_config()

    # Check if config['proxies'] is defined
    if 'proxies' in config:
        proxies = {
            "http": config['proxies']['http'],
            "https": config['proxies']['https'],
        }
    else:
        proxies = None

    if api_key is None:
        try:
            api_key = config['api_keys']['openrouteservice_api_key']
        except KeyError:
            return {'error': 'No API key found in config.ini'}

    try:
        sslVerify = config['ssl']['verify']
    except KeyError:
        sslVerify = 'true'

    return OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=(sslVerify.lower == 'true'))

def calculate_route(positions, profile='foot-walking', api_key=None):
    ors = get_open_route_service(api_key=api_key)

    # Afficher le résultat à l'utilisateur
    distances_matrix = ors.get_distances_matrix(positions, profile=profile)

    optimal_route = get_optimal_route(
        positions, distances_matrix=distances_matrix)

    ors_resp = ors.get_directions(optimal_route, profile=profile)
    geometry = ors_resp.get_geometry()

    return {'optimal_route': optimal_route, 'route': geometry, 'distances_matrix': distances_matrix, 'ors_resp': ors_resp.response}

@app.route('/api/calculate', methods=['POST', 'GET'])
def calculate_route_api():
    positions = request.json['positions']
    # check if positions has at least 2 points
    if len(positions) < 2:
        return {'error': 'At least 2 positions are required'}
    try:
        api_key = request.json['parameters']['api_key']
    except KeyError:
        return {'error': 'No API key provided'}
    
    try:
        profile = request.json['parameters']['profile']
    except KeyError:
        return {'error': 'No profile provided'}
    
    return calculate_route(positions, profile=profile, api_key=api_key)

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
