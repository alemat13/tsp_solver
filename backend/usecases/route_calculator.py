from typing import List, Optional
from ..domain.entities import Point
from ..domain.services import RoutingService
from ..tsp_genetic.tsp import solve_tsp_genetic
from ..app_utils import get_solver_tour_concorde


def get_optimal_route(points: List[Point], distances_matrix=None, population_size: int = 1000, num_generations: int = 300) -> List[Point]:
    coords = [(p.lat, p.lng) for p in points]
    try:
        tour_indices = get_solver_tour_concorde(coords, distances_matrix=distances_matrix)
    except ImportError:
        tour_indices = solve_tsp_genetic(coords, population_size=population_size, num_generations=num_generations, distances_matrix=distances_matrix)
    return [points[i] for i in tour_indices]


def calculate_route(points: List[Point], routing_service: RoutingService, profile: str = 'foot-walking', population_size: int = 1000, num_generations: int = 300):
    distances_matrix = routing_service.get_distances_matrix(points, profile=profile)
    optimal_route = get_optimal_route(points, distances_matrix=distances_matrix, population_size=population_size, num_generations=num_generations)
    directions = routing_service.get_directions(optimal_route, profile=profile)
    geometry = directions.get_geometry()
    return {
        'optimal_route': optimal_route,
        'route': geometry,
        'distances_matrix': distances_matrix,
        'ors_resp': directions.response
    }
