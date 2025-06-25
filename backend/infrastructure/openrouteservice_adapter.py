from typing import List, Optional
import configparser
from ..openrouteservice import OpenRouteService
from ..domain.entities import Point
from ..domain.services import RoutingService

class OpenRouteServiceAdapter(RoutingService):
    def __init__(self, api_key: Optional[str] = None):
        self.service = self._create_service(api_key)

    def _create_service(self, api_key: Optional[str]):
        config = configparser.ConfigParser()
        config.read('config.ini')
        proxies = None
        if 'proxies' in config:
            proxies = {
                'http': config['proxies'].get('http'),
                'https': config['proxies'].get('https')
            }
        if api_key is None:
            api_key = config.get('api_keys', 'openrouteservice_api_key', fallback=None)
            if api_key is None:
                raise ValueError('No API key provided and none found in config.ini')
        verify_ssl = config.getboolean('ssl', 'verify', fallback=True)
        return OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=verify_ssl)

    def get_distances_matrix(self, locations: List[Point], profile: str = 'foot-walking'):
        coords = [(p.lat, p.lng) for p in locations]
        return self.service.get_distances_matrix(coords, profile=profile)

    def get_directions(self, locations: List[Point], profile: str = 'foot-walking'):
        coords = [(p.lat, p.lng) for p in locations]
        return self.service.get_directions(coords, profile=profile)
