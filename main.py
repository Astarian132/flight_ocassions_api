import datetime
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager



# ------------------------ BODY ----------------------------------------#
def update_iata_codes():

    for city in flight_sheety.cur_sheet:
        payload = {
            "term": city['city'],
            "locale": "en-US",
            "location_types": "airport",
            "limit": 10,
            "active_only": "true",
            "sort": "name"
        }

        iata_code = flight_searcher.get_iata(payload)
        flight_sheety.update_sheet(city, iata_code)
        #print(put_response.text)

def check_flights():

    for city in flight_sheety.cur_sheet:
        payload = {
            "fly_from": "LON",
            "fly_to": city['iataCode'],
            "date_from": (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
            "date_to": (datetime.datetime.today() + datetime.timedelta(days=211)).strftime('%d/%m/%Y'),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "adults": 1,
            "one_for_city": 1,
            "curr": "GBP",
            "flight_type": "round"
        }
        try:
            (dest_city, price, link, origin_prefix, destination_prefix) = flight_searcher.check_flights(payload=payload)
        except IndexError:
            try:
                (dest_city, price, link, origin_prefix, destination_prefix) = flight_searcher.check_flights(payload=payload)
            except IndexError:
                print(f"Flight to {city['name']} haven't been found, please try again.")
        if city['lowestPrice'] > price:
            encoded_msg = (f"""Subject:Price Allert! \n\nCheap flight from {flight_searcher.origin_city} ({origin_prefix}) to {dest_city} ({destination_prefix}) for only {price}£! Check offer on {link}""").encode('utf-8', 'ignore')
            notification_sender.send_notification(encoded_msg)
            #print(type(encoded_msg))
    flight_sheety.get_data()



if __name__ == "__main__":
    flight_sheety = DataManager()
    flight_searcher = FlightSearch()
    notification_sender = NotificationManager()
    if flight_sheety.get_data():    # check if any iataCode is missing.
        update_iata_codes()         # update every iata if single one doesn't exist.




