import requests
import pandas as pd
import Query

class connect:
    def __init__(self, location):
        self.__key = 'AIzaSyARK-xnPLJLPKgzz1Vsu9T-AYh2QI5wvZg'
        self.location = location

    def google_api(self, tag, open_now, price):
        query = Query.query(self.location, self.__key, price, tag, open_now).get_query()
        r = requests.get(query)
        if r.status_code == 200:
            p = r.json()['results']
            data = pd.DataFrame(p)
        else:
            print('Cannot make request -- retrying')
            d, status_code = self.get_response(query)
            if status_code != 200:
                print('Could not connect')
                raise ConnectionError
            else:
                return d
        return data, r.status_code


q = connect({'lng': '54.980221', 'lat': '-1.629690'})
df = q.google_api("night_club", True, '2')
pd.set_option('display.max_columns', None)
print(df)
