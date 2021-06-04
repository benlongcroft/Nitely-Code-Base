import requests
import pandas as pd
import Query
from google.cloud import error_reporting

class connect:
    """
    EAVSS connection class. Provides access to EAVSS and Google Places API
    """
    def __init__(self):
        self.__key = 'AIzaSyARK-xnPLJLPKgzz1Vsu9T-AYh2QI5wvZg'
        self.location = None

    @staticmethod
    def __report_manual_error(error_message):
        """
        Reports an error to the google cloud error reporting system for logging
        :param error_message: The error string to be recorded
        """
        try:
            client = error_reporting.Client()
            client.report(error_message)
        except Exception as e:
            print("Error when reporting to Google cloud... ")
            print(e)

    def __make_request(self, query):
        """
        Makes request based on query
        :param query: query string to use
        :return: requests object of page
        """
        r = requests.get(query)
        if r.status_code == 200:
            return r.json()
        else:
            print('Cannot make request -- retrying')
            d = self.__make_request(query)
            if d.status_code != 200:
                error_string = "Could not make request, " \
                               "status code: "+d.status_code+" Reason: "+d.reason
                print(error_string)
                print("Reporting error through Google cloud\n")
                self.__report_manual_error(error_string)
                return None
            else:
                return d.json()

    def google_api(self, location, tag, open_now, price):
        """
        Makes Google API request
        :param location: The location to search near
        :param tag: The tags to include in the query
        :param open_now: open_now bool option to filter for venues that are open
        :param price: price point of the user (Google Maps 0-4 rating)
        :return: Pandas dataframe of information
        """
        query = Query.query(location, self.__key, price, tag, open_now)
        data = self.__make_request(query)
        df = pd.DataFrame(data['results'])
        return df

    def get_timings_from_api(self, venue_id):
        """
        Gets timings data from Google Places Details API
        :param venue_id: The Place ID of the venue
        :return: Opening hours of the venue JSON
        """
        base = "https://maps.googleapis.com/maps/api/place/details/json?"
        query = base + "place_id="+venue_id + "&key="+self.__key
        data = self.__make_request(query)
        data = data['result']
        if 'opening_hours' in data.keys():
            return data['opening_hours']
        else:
            return 0




# q = connect({'lng': '54.980221', 'lat': '-1.629690'})
# df = q.get_timings_from_api("ChIJyRZpVbRwfkgROeXBzOeaUoI")
# pd.set_option('display.max_columns', None)
# print(df)
