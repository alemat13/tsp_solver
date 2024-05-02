import configparser
import itertools
import requests
import json
import os
import threading

def get_config():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config

def get_journeys(start_point, end_point, region_id, include_stepfree, departure_time=None, proxies=None, sslVerify=True):
    url = "https://citymapper.com/api/7/journeys"
    params = {
        "start": start_point,
        "end": end_point,
        "region_id": region_id,
        "include_stepfree": include_stepfree
    }
    if departure_time:
        params["departure_time"] = departure_time
    response = requests.get(url, params=params, proxies=proxies, verify=sslVerify)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des trajets:", response.status_code)
        return None

# Fonction pour récupérer les trajets pour une combinaison de points
def get_journeys_for_combinations(combinations, region_id, include_stepfree, departure_time=None, proxies=None, sslVerify=True):
    for start_point, end_point in combinations:
        output_file = f"journeys_results/{start_point.replace(',', '_')}_to_{end_point.replace(',', '_')}.json"
        print(f"Récupération des trajets de {start_point} à {end_point}...")
        print(f"Avancement: {combinations.index((start_point, end_point)) + 1}/{len(combinations)}")
        journeys = get_journeys(start_point, end_point, region_id, include_stepfree, departure_time, proxies, sslVerify)
        if journeys:
            with open(output_file, "w") as f:
                json.dump(journeys, f, indent=2)

def start_threads(combinations, region_id, include_stepfree, num_threads, departure_time=None, proxies=None, sslVerify=True):
    threads = []
    for i in range(num_threads):
        start = i * len(combinations) // num_threads
        end = (i + 1) * len(combinations) // num_threads
        thread = threading.Thread(target=get_journeys_for_combinations, args=(combinations[start:end], region_id, include_stepfree, departure_time, proxies, sslVerify))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# Liste des points GPS depuis roma.json
with open('roma.json', 'r') as file:
    gps_points = json.load(file)

departure_time = "2024-05-04T10:00:00"

# Générer toutes les combinaisons possibles de points GPS dans les 2 sens
combinations = list(itertools.combinations(gps_points, 2)) + list(itertools.combinations(gps_points[::-1], 2))

# mkdir journeys_results if not exists
if not os.path.exists("journeys_results"):
    os.makedirs("journeys_results")


config = get_config()

# Check if config['proxies'] is defined
if 'proxies' in config:
    proxies = {
        "http": config['proxies']['http'],
        "https": config['proxies']['https'],
    }
else:
    proxies = None

try:
    sslVerify = not(config['ssl']['verify'] == 'false')
except KeyError:
    sslVerify = 'true'

start_threads(combinations, region_id="it-rome", include_stepfree=1, num_threads=100, departure_time=departure_time, proxies=proxies, sslVerify=sslVerify)
print("Tous les trajets ont été récupérés.")
