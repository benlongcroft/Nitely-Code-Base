import datetime
from geopy.distance import geodesic
import pandas as pd


class GetVenueVectors:
    def __init__(self, smartness, paid, date, TwentyOnePlus, location, location_distance, keywords):
        self.paid = paid
        self.twenty_one_plus = TwentyOnePlus
        self.keywords = keywords
        self.location = {'lat': location.split(",")[0], 'lng': location.split(",")[1]}
        if location_distance > 50:
            print("Distance is too far to accurately represent club_data")
        else:
            self.total_distance_to_travel = location_distance
        try:
            self.LocationCoordinates = location.split(',')
        except Exception as e:
            print('Error splitting coordinates')
            print(e)
        if (smartness <= 5) or (smartness >= 1):
            self.smartness = smartness
        else:
            print('Smartness value is not within valid range')
        try:
            _format_str = '%d%m%Y'
            # should be in format DDMMYYYY
            _date_str = date
            _datetime_obj = datetime.datetime.strptime(_date_str, _format_str)  # converts date into datetime object
            self.date = _datetime_obj.date()
        except Exception as e:
            print('Error when transferring into datetime object')
            print(e)

    @staticmethod
    def __GetDistanceBetweenAddress(current_location, y_coordinates):
        # use geopy geodesic module to get distance in miles and return it to function call
        return geodesic((y_coordinates['lat'], y_coordinates['lng']),
                        (current_location['lat'], current_location['lng'])).miles

    def FetchValidVenues(self, start_location, cursor_obj):
        _command = '''SELECT * FROM venues WHERE dress_rating <= ?'''  # generate base command
        if start_location is not None:
            _location_coordinates = start_location
        else:
            _location_coordinates = self.location
        if self.twenty_one_plus:
            _command = _command + ''' AND age_restriction = "over 21s"'''
        if not self.paid:
            _command = _command + ''' AND entry_price = no door charge'''
        cursor_obj.execute(_command, (self.smartness,))  # execute command

        _fields = ["venue_id", "name", "description", "venue_type",
                  "age_restriction", "entry_price", "dress_code",
                  "dress_rating", "address", "distance"]

        valid_venues_df = pd.DataFrame(columns=_fields)  # create pandas dataframe

        for _record in cursor_obj.fetchall():
            _record = list(_record)  # turn record from tuple to list
            __record_coordinates = {'lat': _record[-1].split(",")[0],
                                  'lng': _record[-1].split(",")[1]}  # get coordinates and split them into a dictionary
            _distance = self.__GetDistanceBetweenAddress(_location_coordinates,
                                                      __record_coordinates)  # get distance between address and venues
            if _distance <= self.total_distance_to_travel:
                _record.append(_distance)
                _record = pd.DataFrame([_record], columns=_fields)  # turn record into df so it can be appended
                valid_venues_df = valid_venues_df.append(_record, ignore_index=True)  # add series to pandas df
        valid_venues_df.sort_values(by=['distance'], inplace=True,
                                    ignore_index=True)  # sort by distance from current location
        return valid_venues_df

    def Get(self, valid_venues_df, cursor_obj):
        _command = '''SELECT vector FROM venue_vectors WHERE venue_id = ?''' # base command for fetching vectors
        _vectors=[] # to collect vectors in temporarily
        for _id in valid_venues_df['venue_id']:
            cursor_obj.execute(_command, (_id,)) # get vector from db for id
            _vectors.append(cursor_obj.fetchall()[0])
        valid_venues_df['vector'] = _vectors # add new column to valid venues to contain vectors
        return valid_venues_df





