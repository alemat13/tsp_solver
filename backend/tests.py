from app import calculate_route, get_optimal_route

positions = [
        [48.8606, 2.3376], # Louvre
        [48.8530, 2.3499], # Notre-Dame
        [48.8738, 2.2950], # Sacré-Cœur
        [48.8867, 2.3431], # La Villette
        [48.8600, 2.3267], # Opéra
        [48.8698, 2.3075], # Canal Saint-Martin
        [48.8635, 2.3274], # Palais Royal
        [48.8462, 2.3447], # Gare Montparnasse
        [48.8656, 2.3212], # Place Vendôme
        [48.8556, 2.3158], # Place de la Concorde
    ]

route = calculate_route(positions)
distance_matrix = [
    [0.0, 1575.09, 3784.34, 3327.81, 1045.76, 2750.32, 924.9, 1997.64, 1819.7, 2235.21],
    [1575.09, 0.0, 5159.62, 4393.63, 2108.23, 4092.34, 2446.9, 1227.96, 3159.47, 2915.14],
    [3784.34, 5159.62, 0.0, 4395.48, 3132.1, 1089.56, 2999.41, 5462.53, 2193.99, 3124.68],
    [3327.81, 4393.63, 4395.48, 0.0, 3783.92, 3911.33, 3280.58, 5214.61, 3442.39, 4708.73],
    [1045.76, 2108.23, 3132.1, 3783.92, 0.0, 2064.83, 666.61, 2377.76, 1141.84, 1237.75],
    [2750.32, 4092.34, 1089.56, 3911.33, 2064.83, 0.0, 1965.39, 4395.25, 1148.63, 2139.57],
    [924.9, 2446.9, 2999.41, 3280.58, 666.61, 1965.39, 0.0, 2761.2, 980.38, 1591.41],
    [1997.64, 1227.96, 5462.53, 5214.61, 2377.76, 4395.25, 2761.2, 0.0, 3392.04, 2765.08],
    [1819.7, 3159.47, 2193.99, 3442.39, 1141.84, 1148.63, 980.38, 3392.04, 0.0, 1430.08],
    [2235.21, 2915.14, 3124.68, 4708.73, 1237.75, 2139.57, 1591.41, 2765.08, 1430.08, 0.0]
]
print(route)
