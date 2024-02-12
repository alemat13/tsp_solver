from concorde.tsp import TSPSolver
fname = "tsp/roma68.tsp"
solver = TSPSolver.from_tspfile(fname)
solution = solver.solve()
print(solution.found_tour)
print(solution.optimal_value)
print(solution.tour)
