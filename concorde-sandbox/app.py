from concorde.problem import Problem
from concorde.tsp import TSPSolver

def get_solver_tour_concorde(points, distances_matrix = None):
    if(distances_matrix is None):
        print(points)
        solver = TSPSolver.from_data(
            [p[0] for p in points],
            [p[1] for p in points],
            norm="GEO"
        )
    else:
        import tempfile, os
        ccdir = tempfile.mkdtemp()
        ccfile = os.path.join(ccdir, "data.tsp")
        Problem.from_matrix(distances_matrix).to_tsp(ccfile)
        solver = TSPSolver.from_tspfile(ccfile)
    try:
        tour_data = solver.solve()
        return tour_data.tour
    # return error message
    except Exception as e:
        print(str(e))
        return {'error': str(e)}


def get_optimal_route(positions, distances_matrix = None):
    # Calculer le chemin optimal avec Concorde
    tour_indices = get_solver_tour_concorde(positions, distances_matrix = distances_matrix)

    # Renvoyer les positions dans l'ordre du chemin optimal
    return [positions[i] for i in tour_indices]

if __name__ == '__main__':
    route = get_optimal_route(debug=True, host='0.0.0.0')
    print(route)
