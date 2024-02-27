from flask import Flask, Response, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_solver_tour_concorde(points):
    from concorde.tsp import TSPSolver
    print(points)
    solver = TSPSolver.from_data(
        [p[0] for p in points],
        [p[1] for p in points],
        norm="GEO"
    )
    tour_data = solver.solve()
    return tour_data.tour

def get_solver_tour_genetic(points, population_size=100, num_generations=100):
    from tsp_genetic import solve_tsp_genetic
    return solve_tsp_genetic(points, population_size, num_generations)

@app.route('/generate_kml', methods=['POST'])
def generate_kml():
    # Récupérer les positions GPS entrées par l'utilisateur
    positions = request.form.get('positions').splitlines()

    # Convertir les positions en un format utilisable par Concorde
    # Supposons que les positions sont des tuples (latitude, longitude)
    points = [(float(pos.split(',')[0]), float(pos.split(',')[1])) for pos in positions]

    # Données à utiliser pour générer le KML (exemple)
    data = {
        'lines': [
            {
                'name': 'Line 1',
                'coordinates': points
            },
        ]
    }

    # Rendu du template avec les données
    kml_content = render_template('map.kml', data=data)
    # Définir le type de contenu comme application/vnd.google-earth.kml+xml
    # pour indiquer qu'il s'agit d'un fichier KML
    return Response(
        kml_content,
        mimetype='application/vnd.google-earth.kml+xml',
        headers={'Content-Disposition': 'attachment; filename=' + 'map.kml'}
    )

def get_optimal_route(points):
# Calculer le chemin optimal avec Concorde
    try:
        tour_indices = get_solver_tour_concorde(points)
    except ImportError:
        tour_indices = get_solver_tour_genetic(points, population_size=10000, num_generations=1000)

    # Renvoyer les positions dans l'ordre du chemin optimal
    return [points[i] for i in tour_indices]

@app.route('/api/calculate', methods=['POST', 'GET'])
def calculate_route_api():
    
    # Récupérer les positions GPS entrées par l'utilisateur
    positions = request.json

    # Convertir les positions en un format utilisable par Concorde
    # points = [(float(pos.split(',')[0]), float(pos.split(',')[1])) for pos in positions]
    
    # Afficher le résultat à l'utilisateur
    return get_optimal_route(positions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
