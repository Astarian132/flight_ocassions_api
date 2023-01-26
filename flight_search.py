import dotenv
import requests

class FlightSearch:
    def __init__(self) -> None:
        self.origin_city = "London"
        self.origin_iata = "Lon"
        self.tequila_token = dotenv.dotenv_values("python.env").get('tequila_token')
        self.tequila_location_url = "https://api.tequila.kiwi.com"
        self.tequila_booking_token = dotenv.dotenv_values("python.env").get('tequila_booking_token')
        self.tequila_header = {
            "apikey": self.tequila_token,
            "Content-Encoding": "gzip",
            "Content-Type": "application/json"
        }

        self.tequila_booking_header = {
            "apikey": self.tequila_booking_token,
            "Content-Encoding": "gzip",
            "Content-Type": "application/json"
        }

    def get_iata(self, payload:dict) -> str:
        response = requests.get(url=f"{self.tequila_location_url}/locations/query", headers=self.tequila_header, params=payload)
        return response.json()['locations'][0]['city']['code']

    def check_flights(self, payload:dict) -> tuple:
        self.flights = requests.get(url=f"{self.tequila_location_url}/v2/search", headers=self.tequila_booking_header, params=payload).json()['data']
        city = self.flights[0]['cityTo']
        price = self.flights[0]['price']
        link = self.flights[0]['deep_link']
        origin_prefix  = self.flights[0]['flyFrom']
        destination_prefix = self.flights[0]['flyTo']
        return (city, price, link, origin_prefix, destination_prefix)