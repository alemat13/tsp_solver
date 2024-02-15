from flask import Flask, render_template, request

app = Flask(__name__)

# Page d'accueil de l'application
@app.route('/')
def index():
    return render_template('index.html')

def get_solver_tour_concorde(points):
    from concorde.tsp import TSPSolver
    solver = TSPSolver.from_data(points[:, 0], points[:, 1], norm="GEO")
    tour_data = solver.solve()
    return tour_data.tour

def get_solver_tour_mock(points):
    import random
    points_rand = list(range(0, len(points)))
    random.shuffle(points_rand)
    return points_rand

# Route pour traiter le formulaire et afficher le chemin optimal
@app.route('/calculate', methods=['POST'])
def calculate_route():
    
    # Récupérer les positions GPS entrées par l'utilisateur
    positions = request.form.get('positions').splitlines()
    

    # Convertir les positions en un format utilisable par Concorde
    # Supposons que les positions sont des tuples (latitude, longitude)
    points = [(float(pos.split(',')[0]), float(pos.split(',')[1])) for pos in positions]

    # Calculer le chemin optimal avec Concorde
    try:
        tour_indices = get_solver_tour_concorde(points)
    except ImportError:
        tour_indices = get_solver_tour_mock(points)

    print([points, tour_indices])
    # Renvoyer les positions dans l'ordre du chemin optimal
    optimal_route = [points[i] for i in tour_indices]

    # Afficher le résultat à l'utilisateur
    return render_template('result.html', optimal_route=optimal_route)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
