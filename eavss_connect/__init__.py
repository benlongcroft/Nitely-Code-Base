import requests
import pandas as pd
import os
import Query
import pickle
from google.cloud import error_reporting

class connect:
    """
    EAVSS connection class. Provides access to EAVSS and Google Places API
    """
    def __init__(self, db):
        self.__key = 'YOURKEYHERE'
        self.location = None
        self.db_obj = db
        self.cursor = self.db_obj.cursor()
        self.filestore_path = "PATH_TO_FILESTORE"

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

    def get_EAVSS_vectors(self, venues):
        venue_ids = {}
        for venue in venues:
            maps_place_id = venue.get_id
            self.cursor.execute("""SELECT venue_id FROM main.venues WHERE place_id = ?""", (maps_place_id,))
            r = self.cursor.fetchall()
            if len(r) == 0:
                print("VENUE NOT IN DB")
            else:
                venue_ids[r[0]] = venue

        updated_venues = []
        vectors = os.listdir()
        for pk in venue_ids.keys():
            venue = venue_ids[pk]
            if pk in vectors:
                infile = open(self.filestore_path+"/VEC/"+pk, "rb")
                updated_venues.append(
                    venue.set_vector(
                        pickle.load(infile)))
                infile.close()

        return updated_venues

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
        try:
            opening_hours = data['opening_hours']
        except KeyError:
            opening_hours = 0
        return opening_hours




# q = connect()
# q.location = {'lng': '54.980221', 'lat': '-1.629690'}
# df = q.get_timings_from_api("ChIJyRZpVbRwfkgROeXBzOeaUoI")
# pd.set_option('display.max_columns', None)
# print(df)
