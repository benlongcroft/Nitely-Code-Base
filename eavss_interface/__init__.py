import requests
import pandas as pd
import Query

class connect:
    def __init__(self, location):
        self.__key = 'AIzaSyARK-xnPLJLPKgzz1Vsu9T-AYh2QI5wvZg'
        self.location = location

    def __make_request(self, query):
        r = requests.get(query)
        if r.status_code == 200:
            return r.json()
        else:
            print('Cannot make request -- retrying')
            d, status_code = self.get_response(query)
            if status_code != 200:
                print('Could not connect')
                raise ConnectionError
            else:
                return d

    def google_api(self, tag, open_now, price):
        query = Query.query(self.location, self.__key, price, tag, open_now).get_query()
        data = self.__make_request(query)
        df = pd.DataFrame(data['results'])
        return df

    def get_timings_from_api(self, venue_id):
        base = "https://maps.googleapis.com/maps/api/place/details/json?"
        query = base + "place_id="+venue_id + "&key="+self.__key
        data = self.__make_request(query)
        data = data['result']
        if 'opening_hours' in data.keys():
            return data['opening_hours']
        else:
            print('No opening hours...')
            return 0




# q = connect({'lng': '54.980221', 'lat': '-1.629690'})
# df = q.get_timings_from_api("ChIJyRZpVbRwfkgROeXBzOeaUoI")
# pd.set_option('display.max_columns', None)
# print(df)
