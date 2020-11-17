import datetime
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import sqlite3
from . import intensity


class GetVenueVectors:
    def __init__(self, smartness, paid, date,
                 eighteen, location, location_distance,
                 keywords, gay):
        self.__paid = paid
        self.__eighteen = eighteen
        self.__keywords = keywords
        self.__location = {'lat': location.split(",")[0], 'lng': location.split(",")[1]}
        self.__gay = gay
        db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
        self.cursor_obj = db_obj.cursor()  # instantiate a cursor for db

        if location_distance > 50:
            print("Distance is too far to accurately represent club_data")
        else:
            self.__total_distance_to_travel = location_distance

        try:
            self.__LocationCoordinates = location.split(',')
        except Exception as e:
            print('Error splitting coordinates')
            print(e)

        if (smartness <= 5) or (smartness >= 1):
            self.__smartness = smartness
        else:
            print('Smartness value is not within valid range')

        try:
            _format_str = '%d%m%Y'
            # should be in format DDMMYYYY
            _date_str = date
            _datetime_obj = datetime.datetime.strptime(_date_str, _format_str)  # converts date into datetime object
            self.__date = _datetime_obj.date()
        except Exception as e:
            print('Error when transferring into datetime object')
            print(e)

    @property
    def get_keywords(self):
        return self.__keywords

    @staticmethod
    def __GetDistanceBetweenAddress(current_location, y_coordinates):
        # use geopy geodesic module to get distance in miles and return it to function call
        return geodesic((y_coordinates['lat'], y_coordinates['lng']),
                        (current_location['lat'], current_location['lng'])).miles

    def FetchValidVenues(self, start_location, radius):
        _command = '''SELECT * FROM venues WHERE dress_rating <= ?'''  # generate base command
        if start_location is not None:
            location_coordinates = start_location
        else:
            location_coordinates = self.__location

        if radius is None:
            radius = self.__total_distance_to_travel

        # sort out how far and where from where the user wants to travel
        if self.__gay:
            _command = _command + ''' AND NOT gay = 1'''
        if self.__eighteen:
            _command = _command + ''' AND NOT age_restriction = "over 21s"'''
        if not self.__paid:
            _command = _command + ''' AND entry_price = no door charge'''

        # add to base command based on user preferences
        self.cursor_obj.execute(_command, (self.__smartness,))  # execute comand

        _fields = ["venue_id", "name", "description", "venue_type",
                   "age_restriction", "entry_price", "dress_code",
                   "dress_rating", "address", "distance"]

        valid_venues_df = pd.DataFrame(columns=_fields)  # create pandas dataframe

        for record in self.cursor_obj.fetchall():
            record = list(record)  # turn record from tuple to list
            record_coordinates = {'lat': record[-1].split(",")[0],
                                  'lng': record[-1].split(",")[1]}  # get coordinates and split them into a dictionary
            distance = self.__GetDistanceBetweenAddress(location_coordinates,
                                                        record_coordinates)  # get distance between address and venues
            if distance <= radius:
                record.append(distance)
                record = pd.DataFrame([record], columns=_fields)  # turn record into df so it can be appended
                valid_venues_df = valid_venues_df.append(record, ignore_index=True)  # add series to pandas df
        return valid_venues_df

    def GetVectors(self, vector_ids):
        _command = '''SELECT vector FROM venue_vectors WHERE venue_id = ?'''  # base command for fetching vectors
        _vectors = []  # to collect vectors in temporarily
        for x in vector_ids:
            self.cursor_obj.execute(_command, (x,))  # get vector from db for id
            _vectors.append(self.cursor_obj.fetchall()[0])  # add new column to valid venues to contain vectors
        return _vectors


    @staticmethod
    def __RemoveVenue(df, venue_id):
        try:
            index = df[df['venue_id'] == venue_id].index[0]  # get index of venue_to_add
            df = df.drop(index)  # remove locally from df so that we don't choose the same venue twice
        except IndexError:
            print(venue_id, 'already removed from df')
        return df

    # TODO: Fix this utter piece of shit
    def AlterIntensity(self, df, venue, position_in_night, total_venues):
        if position_in_night == 0:
            if not (intensity.check_venue_music_type(venue, self.cursor_obj, [2, 4, 5, 7, 9], [1, 2, 3, 5, 6, 13, 15, 17, 18])):
                for index, row in df.iterrows():
                    if intensity.check_venue_music_type(row, self.cursor_obj, [2, 4, 5, 7, 9], [1, 2, 3, 5, 6, 13, 15, 17, 18]):
                        venue = row
                        break

        elif position_in_night == total_venues - 1:
            if not intensity.check_venue_music_type(venue, self.cursor_obj, [1, 11], [4, 7, 8, 9, 10, 11, 12, 14, 16, 19, 20, 21]):
                for index, row in df.iterrows():
                    if intensity.check_venue_music_type(row, self.cursor_obj, [1, 11], [4, 7, 8, 9, 10, 11, 12, 14, 16, 19, 20, 21]):
                        venue = row
                        break

        return venue

    def GetNextVenue(self, K2KObj, venue_to_add, user_vector, df, package, num_venues, n):
        if n == num_venues:
            return package
        else:
            correct_venue = self.AlterIntensity(df, venue_to_add, n, num_venues)
            if correct_venue['venue_id'] != venue_to_add['venue_id']:
                print('Changed', venue_to_add['name'], 'to', correct_venue['name'])
                venue_to_add = correct_venue

            # check if venue is the correct level of intensity
            package = package.append(venue_to_add, ignore_index=True)

            vector = np.array([float(x) for x in venue_to_add['vector'][0].split(' ')]).reshape(1, 300)
            # Get vector from venue_to_add (comes in string format so takes a bit of rejigging)
            composite_vector = K2KObj.CompositeVector([user_vector, vector])
            # create composite vector of user vector and venues vector

            location = {'lat': venue_to_add['address'].split(",")[0], 'lng': venue_to_add['address'].split(",")[1]}
            # get the location of the club

            df = self.FetchValidVenues(location, radius=1)

            # remove venues already in our package. Don't wanna return to a venue
            for venue_id in package['venue_id']:
                df = self.__RemoveVenue(df, venue_id)

            # add vectors to df
            df['vector'] = self.GetVectors(list(df['venue_id']))

            # find clubs within a mile of the starting club to begin search for the next club
            df = K2KObj.GetClosestVectors(df, composite_vector)
            print(len(df))
            next_venue = df.iloc[0]

            return self.GetNextVenue(K2KObj, next_venue, user_vector, df, package, num_venues, n + 1)
