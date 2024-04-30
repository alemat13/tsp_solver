import requests

from .journey import Journey

class Client:
    def __init__(self, api_url: str = "https://citymapper.com/api/7"):
        self.api_url = api_url
        

    def get_journey(self, start_coords: tuple, end_coords: tuple, time: str = None) -> Journey:
        # Prepare the request body
        body = {
            "start_coord": ",".join(start_coords),
            "end_coord": ",".join(end_coords),
            "time": time
        }

        call = requests.get(
            url=f'{self.api_url}/journey',
            json=body
        )
        return Journey(call.json())
    
if __name__ == "__main__":
    client = Client()
    journey = client.get_journey(
        start_coords=(51.525246, -0.084672),
        end_coords=(51.559098, -0.074503)
    )
    print(journey.duration)
    print(journey.arrival_time)
    print(journey.departure_time)
    print(journey.start_coords)
    print(journey.end_coords)
    print(journey.start_address)
    print(journey.end_address)
    print(journey.steps)
    print(journey.distance)
    print(journey.cost)