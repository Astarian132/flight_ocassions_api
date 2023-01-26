import dotenv
import requests

class DataManager:
    def __init__(self) -> None:
        self.sheety_endpoint = "https://api.sheety.co/064db4819f45aa138522dce77f265f86/flightDeals/prices"
        self.sheety_token = dotenv.dotenv_values("python.env").get('sheety_flight_token')
        self.sheety_header = {
            "Authorization": "Bearer " + self.sheety_token
        }

    def get_data(self) -> bool:
        self.cur_sheet = requests.get(url=self.sheety_endpoint, headers=self.sheety_header).json()['prices']
        for i in self.cur_sheet:
            if len(i['iataCode']) == 0:
                return True
        return False

    def update_sheet(self, city, iata_code: str) -> None:
        requests.put(url=f"{self.sheety_endpoint}/{city['id']}", json={"price":{"iataCode": iata_code}}, headers=self.sheety_header)

