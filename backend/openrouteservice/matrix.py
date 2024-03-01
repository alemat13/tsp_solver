import requests
class DistanceMatrix:
    def __init__(self, api_key, proxies = None, verifySsl = True):
        self.api_key = api_key
        self.proxies = proxies
        self.verifySsl = verifySsl

    def get_distances_matrix(self, locations, metrics = ["distance"], units = "m"):
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
            url='https://api.openrouteservice.org/v2/matrix/foot-walking',
            json=body,
            headers=headers,
            proxies=self.proxies,
            verify=self.verifySsl
        )

        return call.json()['distances']

if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read('../config.ini')
    proxies = {
        "http": config['proxies']['http'],
        "https": config['proxies']['https'],
    }
    api_key = config['api_keys']['openrouteservice_api_key']
    dm = DistanceMatrix(api_key=api_key, proxies=proxies, verifySsl=False)

    locations = [
        [2.294481, 48.858370], # Eiffel Tower
        [2.337622, 48.860611], # Louvre Museum
        [2.349014, 48.853000], # Notre-Dame Cathedral
        [2.326705, 48.859961], # Musée d'Orsay
        [2.342620, 48.886217], # Montmartre
        [2.295054, 48.873792], # Arc de Triomphe
        [2.321956, 48.865496], # Concorde Square
        [2.369839, 48.853400], # Bastille
        [2.393376, 48.861393], # Père Lachaise Cemetery
        [2.331389, 48.872500], # Palais Garnier
        [2.367500, 48.855833], # Place des Vosges
        [2.345833, 48.855556], # Sainte-Chapelle
        [2.346111, 48.846389], # Pantheon
        [2.337500, 48.846389], # Luxembourg Gardens
        [2.301944, 48.873889], # Champs-Élysées
    ]

    distances = dm.get_distances_matrix(locations)

    print(distances)
