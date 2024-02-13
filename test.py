import pandas as pd
from concorde.tsp import TSPSolver

def load_data(file_path, delimiter='\t'):
    """
    Load data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        delimiter (str): Delimiter of the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the data loaded from the CSV file.
    """
    csv_data = pd.read_csv(file_path, delimiter=delimiter)
    return csv_data

def solve_tsp(latitudes, longitudes):
    """
    Solve the Traveling Salesman Problem (TSP) using the provided data.

    Args:
        latitudes (pandas.Series): Series containing the latitudes of locations.
        longitudes (pandas.Series): Series containing the longitudes of locations.

    Returns:
        numpy.ndarray: Solution of the TSP.
    """
    solver = TSPSolver.from_data(latitudes, longitudes, norm="GEO")
    solution = solver.solve()
    return solution

def print_solution(data, solution):
    """
    Print the solution of the TSP.

    Args:
        data (pandas.DataFrame): DataFrame containing the original data.
        solution (numpy.ndarray): Solution of the TSP to be printed.
    """
    print(data.iloc[solution.tour].to_csv(index=False, sep='\t'))

def print_kml_line_string(latitudes, longitudes, tour_indices):
    """
    Print the KML Line String for the TSP solution.

    Args:
        latitudes (pandas.Series): Series containing the latitudes of locations.
        longitudes (pandas.Series): Series containing the longitudes of locations.
        tour_indices (numpy.ndarray): Indices of locations in the TSP solution tour.
    """
    print("KML Line String")
    for index in tour_indices:
        print(f"{longitudes[index]},{latitudes[index]}")

def main():
    # Load data from a CSV file
    csv_data = load_data('tsp/roma_without_esrin.csv')

    # Splitting the location columns
    latitudes = csv_data['Localisation'].str.split(',', expand=True)[0]
    longitudes = csv_data['Localisation'].str.split(',', expand=True)[1]

    # Solve the TSP
    solution = solve_tsp(latitudes, longitudes)

    # Print the solution
    print_solution(csv_data, solution)

    # Print the KML Line String
    print_kml_line_string(latitudes, longitudes, solution.tour)

if __name__ == "__main__":
    main()
