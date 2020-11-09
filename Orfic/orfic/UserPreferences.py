import datetime
from geopy.distance import geodesic
import pandas as pd


class GetVenueVectors:
    def __init__(self, smartness, paid, date, TwentyOnePlus, location, location_distance, keywords):
        self.__paid = paid
        self.__twenty_one_plus = TwentyOnePlus
        self.__keywords = keywords
        self.__location = {'lat': location.split(",")[0], 'lng': location.split(",")[1]}
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

    def FetchValidVenues(self, start_location, cursor_obj):
        _command = '''SELECT * FROM venues WHERE dress_rating <= ?'''  # generate base command
        if start_location is not None:
            location_coordinates = start_location
        else:
            location_coordinates = self.__location
        if self.__twenty_one_plus:
            _command = _command + ''' AND age_restriction = "over 21s"'''
        if not self.__paid:
            _command = _command + ''' AND entry_price = no door charge'''
        cursor_obj.execute(_command, (self.__smartness,))  # execute command

        _fields = ["venue_id", "name", "description", "venue_type",
                  "age_restriction", "entry_price", "dress_code",
                  "dress_rating", "address", "distance"]

        valid_venues_df = pd.DataFrame(columns=_fields)  # create pandas dataframe

        for record in cursor_obj.fetchall():
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

    def Get(self, valid_venues_df, cursor_obj):
        _command = '''SELECT vector FROM venue_vectors WHERE venue_id = ?''' # base command for fetching vectors
        _vectors=[] # to collect vectors in temporarily
        for id in valid_venues_df['venue_id']:
            cursor_obj.execute(_command, (id,)) # get vector from db for id
            _vectors.append(cursor_obj.fetchall()[0])
        valid_venues_df['vector'] = _vectors # add new column to valid venues to contain vectors
        return valid_venues_df





