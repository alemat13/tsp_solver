import itertools
import requests
import json
import os
import threading

def get_journeys(start_point, end_point, region_id, include_stepfree, departure_time=None):
    url = "https://citymapper.com/api/7/journeys"
    params = {
        "start": start_point,
        "end": end_point,
        "region_id": region_id,
        "include_stepfree": include_stepfree
    }
    if departure_time:
        params["departure_time"] = departure_time
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des trajets:", response.status_code)
        return None

# Fonction pour récupérer les trajets pour une combinaison de points
def get_journeys_for_combinations(combinations, region_id, include_stepfree, departure_time=None):
    for start_point, end_point in combinations:
        output_file = f"journeys_results/{start_point.replace(',', '_')}_to_{end_point.replace(',', '_')}.json"
        print(f"Récupération des trajets de {start_point} à {end_point}...")
        print(f"Avancement: {combinations.index((start_point, end_point)) + 1}/{len(combinations)}")
        journeys = get_journeys(start_point, end_point, region_id, include_stepfree, departure_time)
        if journeys:
            with open(output_file, "w") as f:
                json.dump(journeys, f)

def start_threads(combinations, region_id, include_stepfree, num_threads, departure_time=None):
    threads = []
    for i in range(num_threads):
        start = i * len(combinations) // num_threads
        end = (i + 1) * len(combinations) // num_threads
        thread = threading.Thread(target=get_journeys_for_combinations, args=(combinations[start:end], region_id, include_stepfree, departure_time))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

# Liste des points GPS
gps_points = [
    "41.8868358,12.5251806",
    "41.8929759,12.5157068",
    "41.88854545,12.52874245",
    "41.8998265,12.51705828",
    "41.918392,12.4790533",
    "41.86334754,12.48041506",
    "41.888757,12.47055392",
    "41.87535495,12.4742397",
    "41.87554,12.54137882",
    "41.8928812,12.5416602",
    "41.88925542,12.52989933",
    "41.88883611,12.51881613",
    "41.88902887,12.52566559",
    "41.91129857,12.49857476",
    "41.93565464,12.50632918",
    "41.9363506,12.46667506",
    "41.90752443,12.45537829",
    "41.89129432,12.47052934",
    "41.88390936,12.47415562",
    "41.87468124,12.52271536",
    "41.91863495,12.50124505",
    "41.8944226,12.4921029",
    "41.88371581,12.47454914",
    "41.89716181,12.51327601",
    "41.89424943,12.50631894",
    "41.89545539,12.49336119",
    "41.8948595,12.4910821",
    "41.89649702,12.51513618",
    "41.8963236,12.5141464",
    "41.89641328,12.48655847",
    "41.8985068,12.48455324",
    "41.9073545,12.4759696",
    "41.90475039,12.47695694",
    "41.88535713,12.50923977",
    "41.89366787,12.47874109",
    "41.89441975,12.4691352",
    "41.88783118,12.49442329",
    "41.89735513,12.48497742",
    "41.89997622,12.47977882",
    "41.90005074,12.47087219",
    "41.8993956,12.4704421",
    "41.9035004,12.4833433",
    "41.9062582,12.4830485",
    "41.862693,12.4855537",
    "41.87870456,12.47898921",
    "41.89347824,12.47688193",
    "41.88974258733448, 12.523768568648917",
    "41.8901019,12.4943457",
    "41.89526328,12.47253642",
    "41.88969098,12.47109886",
    "41.889545,12.473174",
    "41.8794955,12.53691112",
    "41.88938431,12.51955703",
    "41.89953206,12.5012803",
    "41.87325486,12.50166805",
    "41.883822466062824, 12.531461069545676",
    "41.90097148,12.48295787",
    "41.87395366,12.50625287",
]
departure_time = "2024-05-04T10:00:00"

# Générer toutes les combinaisons possibles de points GPS dans les 2 sens
combinations = list(itertools.combinations(gps_points, 2)) + list(itertools.combinations(gps_points[::-1], 2))

# mkdir journeys_results if not exists
if not os.path.exists("journeys_results"):
    os.makedirs("journeys_results")

# Nombre de threads à utiliser pour récupérer les trajets

start_threads(combinations, region_id="it-rome", include_stepfree=1, num_threads=100, departure_time=departure_time)
print("Tous les trajets ont été récupérés.")
