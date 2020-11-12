import datetime
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import sqlite3

class GetVenueVectors:
    def __init__(self, smartness, paid, date, TwentyOnePlus, location, location_distance, keywords):
        self.__paid = paid
        self.__twenty_one_plus = TwentyOnePlus
        self.__keywords = keywords
        self.__location = {'lat': location.split(",")[0], 'lng': location.split(",")[1]}
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

    def FetchValidVenues(self, start_location):
        _command = '''SELECT * FROM venues WHERE dress_rating <= ?'''  # generate base command
        if start_location is not None:
            location_coordinates = start_location
        else:
            location_coordinates = self.__location
        if self.__twenty_one_plus:
            _command = _command + ''' AND age_restriction = "over 21s"'''
        if not self.__paid:
            _command = _command + ''' AND entry_price = no door charge'''
        self.cursor_obj.execute(_command, (self.__smartness,))  # execute command

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
            if distance <= self.__total_distance_to_travel:
                record.append(distance)
                record = pd.DataFrame([record], columns=_fields)  # turn record into df so it can be appended
                valid_venues_df = valid_venues_df.append(record, ignore_index=True)  # add series to pandas df
        valid_venues_df.sort_values(by=['distance'], inplace=True,
                                    ignore_index=True)  # sort by distance from current location
        return valid_venues_df

    def Get(self, valid_venues_df):
        _command = '''SELECT vector FROM venue_vectors WHERE venue_id = ?''' # base command for fetching vectors
        _vectors=[] # to collect vectors in temporarily
        for id in valid_venues_df['venue_id']:
            self.cursor_obj.execute(_command, (id,)) # get vector from db for id
            _vectors.append(self.cursor_obj.fetchall()[0])
        valid_venues_df['vector'] = _vectors # add new column to valid venues to contain vectors
        return valid_venues_df

    @staticmethod
    def __RemoveVenue(df, venue_id):
        index = df[df['venue_id'] == venue_id].index[0]  # get index of venue_to_add
        df = df.drop(index)  # remove locally from df so that we don't choose the same venue twice
        return df


    def GetNextVenue(self, K2KObj, venue_to_add, user_vector, v_df, package, num_venues, n): # add 1 to n
        if n > num_venues-1:  # if number of venues is max
            return package, v_df # return all values
        else:
            if n == 1:
                correct_venue = K2KObj.ReorderForIntensity(v_df, venue_to_add, n,
                                                           num_venues, self.cursor_obj)
                if correct_venue['venue_id'] != venue_to_add['venue_id']:
                    venue_to_add = correct_venue

                v_df = self.__RemoveVenue(v_df, venue_to_add['venue_id'])
                package = package.append(venue_to_add, ignore_index=True)

            n = n + 1
            vector = np.array([float(x) for x in venue_to_add['vector'][0].split(' ')]).reshape(1,300)  # get venues vector
            composite_vector = K2KObj.CompositeVector(user_vector, vector)
            # find midpoint between users vector and venues vector
            v_df = K2KObj.GetClosestVectors(v_df, composite_vector)  # get vector closest to composite vector
            v_df = v_df.rename_axis(None)

            next_venue = v_df.iloc[0]  # get top value as v_df is sorted by similarit
            correct_venue = K2KObj.ReorderForIntensity(v_df, next_venue, n,
                                                       num_venues, self.cursor_obj)

            # print(n+1, correct_venue['venue_id'], next_venue['venue_id'])
            if next_venue['venue_id'] != correct_venue['venue_id']:
                next_venue = correct_venue
            v_df = self.__RemoveVenue(v_df, next_venue['venue_id'])  # remove the venue from the df to prevent it from
            # occuring multiple times within each package just in different orders
            package = package.append(next_venue, ignore_index=True)
            return self.GetNextVenue(K2KObj, next_venue, user_vector, v_df, package, num_venues, n)
            # recursively do again with next venue




