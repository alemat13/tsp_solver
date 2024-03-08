import requests
class OpenRouteService:
    def __init__(self, api_key, proxies = None, verifySsl = True, logger = None):
        self.api_key = api_key
        self.proxies = proxies
        self.verifySsl = verifySsl
        self.logger = logger

    def get_distances_matrix(self, locations, metrics = ["distance"], units = "m", profile = "foot-walking"):
        # Check if profile is valid
        self._check_profile(profile)
        
        # Inverse latitude and longitude
        lngLat = [[lng, lat] for lat, lng in locations]

        # Prepare the request body
        body = {"locations": lngLat,"metrics":metrics,"units":units}

        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': self.api_key,
            'Content-Type': 'application/json; charset=utf-8'
        }
        call = requests.post(
            url=f'https://api.openrouteservice.org/v2/matrix/{profile}',
            json=body,
            headers=headers,
            proxies=self.proxies,
            verify=self.verifySsl
        )

        try:
            return call.json()['distances']
        except:
            self.logger.debug(call.json())
            return None
    
    # Function to check if the profile is valid
    def _check_profile(self, profile):
        if profile not in ['foot-walking', 'cycling-regular', 'driving-car', 'driving-hgv', 'wheelchair', 'cycling-road', 'cycling-mountain', 'cycling-electric', 'cycling-safe', 'cycling-tour', 'cycling-mountain']:
            raise ValueError(f'Invalid profile: {profile}')

    # Get route between points in GeoJSON format
    def get_route(self, locations, profile = "foot-walking"):
        # check if profile is valid
        self._check_profile(profile)
        
        # Inverse latitude and longitude
        lngLat = [[lng, lat] for lat, lng in locations]

        # Prepare the request body & headers
        body = {"coordinates": lngLat}
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': self.api_key,
            'Content-Type': 'application/json; charset=utf-8'
        }

        # Make the request
        call = requests.post(
            url=f'https://api.openrouteservice.org/v2/directions/{profile}/geojson',
            json=body,
            headers=headers,
            proxies=self.proxies,
            verify=self.verifySsl
        )

        # Return the result
        return call.json()
    
    def get_geometry(self, locations, profile = "foot-walking"):
        route = self.get_route(locations, profile=profile)
        geometry = route['features'][0]['geometry']['coordinates']
        return [[lng, lat] for lat, lng in geometry]

if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read('../config.ini')
    proxies = {
        "http": config['proxies']['http'],
        "https": config['proxies']['https'],
    }
    api_key = config['api_keys']['openrouteservice_api_key']
    dm = OpenRouteService(api_key=api_key, proxies=proxies, verifySsl=False)

    locations = [
        [48.858370, 2.294481], # Eiffel Tower
        [48.860611, 2.337622], # Louvre Museum
        [48.853000, 2.349014], # Notre-Dame Cathedral
        [48.859961, 2.326705], # Musée d'Orsay
        [48.886217, 2.342620], # Montmartre
        [48.873792, 2.295054], # Arc de Triomphe
        [48.865496, 2.321956], # Concorde Square
        [48.853400, 2.369839], # Bastille
        [48.861393, 2.393376], # Père Lachaise Cemetery
        [48.872500, 2.331389], # Palais Garnier
        [48.855833, 2.367500], # Place des Vosges
        [48.855556, 2.345833], # Sainte-Chapelle
        [48.846389, 2.346111], # Pantheon
        [48.846389, 2.337500], # Luxembourg Gardens
        [48.873889, 2.301944], # Champs-Élysées
    ]

    distances = dm.get_distances_matrix(locations)
    app.logger.debug(distances)

    route = dm.get_route(locations)
    app.logger.debug(route)
