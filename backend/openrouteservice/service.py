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
    def get_directions(self, locations, profile = "foot-walking"):
        
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
        return OpenRouteService_response(call.json())

class OpenRouteService_response:
    def __init__(self, response):
        self.response = response
    def get_geometry(self):
        geometry = self.response['features'][0]['geometry']['coordinates']
        return [[lng, lat] for lat, lng in geometry]
    def get_response(self):
        return self.response
    def get_distances_matrix(self):
        return self.response['distances']
