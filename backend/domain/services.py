from abc import ABC, abstractmethod
from typing import List
from .entities import Point

class RoutingService(ABC):
    @abstractmethod
    def get_distances_matrix(self, locations: List[Point], profile: str = "foot-walking"):
        pass

    @abstractmethod
    def get_directions(self, locations: List[Point], profile: str = "foot-walking"):
        pass
