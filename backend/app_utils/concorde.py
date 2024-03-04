
from concorde.tsp import TSPSolver
from concorde.problem import Problem
import tempfile, os

def get_solver_tour_concorde(points, distances_matrix = None, logger = None):
    if(distances_matrix is None):
        print(points)
        solver = TSPSolver.from_data(
            [p[0] for p in points],
            [p[1] for p in points],
            norm="GEO"
        )
    else:
        distances_matrix_int = [[int(j) for j in i] for i in distances_matrix]
        ccdir = tempfile.mkdtemp()
        ccfile = os.path.join(ccdir, "data.tsp")
        Problem.from_matrix(distances_matrix_int).to_tsp(ccfile)
        solver = TSPSolver.from_tspfile(ccfile)
    try:
        tour_data = solver.solve()
        return tour_data.tour
    
    # return error message
    except Exception as e:
        if(logger):
            logger.error(str(e))
        return {'error': str(e)}

if __name__ == '__main__':
    samples = [
        {
            'positions': [(1, 1), (2, 2), (3, 3), [4, 4]],
            'distances_matrix': [
                [0, 1, 2, 3],
                [1, 0, 1, 2],
                [2, 1, 0, 1],
                [3, 2, 1, 0]
            ]
        },
        {
            'positions': [(1, 1), (2, 2), (3, 3), [4, 4], [5, 5]],
            'distances_matrix': [
                [0, 1, 2, 3, 4],
                [1, 0, 1, 2, 3],
                [2, 1, 0, 1, 2],
                [3, 2, 1, 0, 1],
                [4, 3, 2, 1, 0]
            ]
        }
    ]
    routes = [get_solver_tour_concorde(sample['positions'], sample['distances_matrix']) for sample in samples]
    print(routes)