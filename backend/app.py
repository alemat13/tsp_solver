from flask import Flask, request, send_from_directory
from flask_cors import CORS
import configparser

from domain.entities import Point
from infrastructure.openrouteservice_adapter import OpenRouteServiceAdapter
from usecases.route_calculator import calculate_route as usecase_calculate_route

REACT_BUILD_DIR = '../frontend/build'

app = Flask(__name__, static_folder=REACT_BUILD_DIR, static_url_path='/')
CORS(app)


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config





def get_open_route_service(api_key=None):
    """Return a routing service adapter configured with parameters from config.ini."""
    # This function is kept for backward compatibility with existing code
    return OpenRouteServiceAdapter(api_key=api_key)

def calculate_route(positions, profile='foot-walking', api_key=None, num_generations=300, population_size=1000):
    """High level helper called by the API endpoint."""
    routing_service = get_open_route_service(api_key=api_key)
    points = [Point(lat=lat, lng=lng) for lat, lng in positions]

    result = usecase_calculate_route(
        points,
        routing_service=routing_service,
        profile=profile,
        population_size=population_size,
        num_generations=num_generations,
    )

    result['optimal_route'] = [[p.lat, p.lng] for p in result['optimal_route']]
    return result

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
    
    try:
        population_size = int(request.json['parameters']['population_size'])
    except KeyError:
        population_size = 1000

    try:
        num_generations = int(request.json['parameters']['num_generations'])
    except KeyError:
        num_generations = 300
    
    return calculate_route(
        positions,
        profile=profile,
        api_key=api_key,
        population_size=population_size,
        num_generations=num_generations
    )

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
