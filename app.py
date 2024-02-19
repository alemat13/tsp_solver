from flask import Flask, Response, render_template, request

app = Flask(__name__)

# Page d'accueil de l'application
@app.route('/')
def index():
    return render_template('index.html')

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

def get_tour_distance_mock(route):
    distance = 0
    for i in range(len(route) -1):
        distance += (((route[i+1][0] - route[i][0]) ** 2) + ((route[i+1][1] - route[i][1]) ** 2)) ** 0.5
    return distance


def get_solver_tour_mock(points):
    import random
    selected_tour = list(range(0, len(points)))
    selected_tour_distance = get_tour_distance_mock([points[i] for i in selected_tour])
    for i in range(0, 10000):
        candidate_tour = selected_tour
        random.shuffle(candidate_tour)
        candidate_tour_distance = get_tour_distance_mock([points[i] for i in candidate_tour])
        if(candidate_tour_distance < selected_tour_distance):
            selected_tour = candidate_tour
            selected_tour_distance = candidate_tour_distance
    return selected_tour

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
        tour_indices = get_solver_tour_mock(points)

    # Renvoyer les positions dans l'ordre du chemin optimal
    return [points[i] for i in tour_indices]

# Route pour traiter le formulaire et afficher le chemin optimal
@app.route('/calculate', methods=['POST'])
def calculate_route():
    
    # Récupérer les positions GPS entrées par l'utilisateur
    positions = request.form.get('positions').splitlines()

    # Convertir les positions en un format utilisable par Concorde
    # Supposons que les positions sont des tuples (latitude, longitude)
    points = [(float(pos.split(',')[0]), float(pos.split(',')[1])) for pos in positions]

    optimal_route = get_optimal_route(points)

    # Afficher le résultat à l'utilisateur
    return render_template(
        'result.html',
        optimal_route=optimal_route,
        optimal_route_ta='\n'.join([str(p[0]) + "," + str(p[1]) for p in optimal_route])
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
