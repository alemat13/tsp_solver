import pandas as pd
from concorde.tsp import TSPSolver

csv_data = pd.read_csv('tsp/roma_without_esrin.csv', delimiter='\t')
localisations = csv_data['Localisation'].str.split(',', expand=True)

solver = TSPSolver.from_data(localisations[0], localisations[1], norm="GEO")
solution = solver.solve()

print(csv_data.iloc[solution.tour].to_csv(index=False,sep='\t'))

print("KML Line String")
[print(x) for x in csv_data.iloc[solution.tour]['Localisation'].str.split(",", expand=True)[[1,0]].apply(lambda x: ",".join(x), axis=1)]
