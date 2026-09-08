from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Point:
    lat: float
    lng: float

@dataclass
class Route:
    points: List[Point]
    geometry: List[List[float]]
