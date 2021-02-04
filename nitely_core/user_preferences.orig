"""
Deals with the user inputs and preferences and fetching venues that match the 'hard' criteria.
Calls K2K when necessary. Gets venue vectors, valid dataframes and returns create_packages

"""
import sqlite3
from geopy.distance import geodesic
import pandas as pd
import numpy as np
from nitely_core import intensity
import datetime
import random

class get_venues:
    """Gets all valid venues K2K can use based on their preferences"""

    def __init__(self, kwargs):
        self.__paid = kwargs['paid']
        self.__eighteen = kwargs['eighteen']
        self.__keywords = kwargs['keywords']
        self.__location = self.str_to_coordinates(kwargs['location'])
        self.__gay = kwargs['gay']
        db_obj = sqlite3.connect('../nitely/ClubDataDB.db')  # connect to database
        self.cursor_obj = db_obj.cursor()  # instantiate a cursor for db

        try:
            _format_str = '%d%m%Y%H:%M'
            # should be in format DDMMYYYY
            _date_str = kwargs['date']
            self.__start = datetime.datetime.strptime(_date_str + kwargs['start_time'],
                                                      _format_str)
            self.__end = datetime.datetime.strptime(_date_str + kwargs['end_time'], _format_str)
            # converts date and time into datetime object

        except Exception as e:
            print('Error when transferring into datetime object')
            print(e)

        if kwargs['location_distance'] > 50:
            print("Distance is too far to accurately represent club_data")
        else:
            self.__total_distance_to_travel = kwargs['location_distance']

        if (kwargs['smartness'] <= 5) or (kwargs['smartness'] >= 1):
            self.__smartness = kwargs['smartness']
        else:
            print('Smartness value is not within valid range')

    @property
    def get_keywords(self):
        """Returns keywords"""
        return self.__keywords

    @staticmethod
    def __get_distance_between_address(current_location, y_coordinates):
        """
        Gets distance as crow flies between two addresses

        :param current_location: Users current location in coordinates
        :param y_coordinates: location to travel to in coordinates
        :return: Distance in miles between coordinates
        """
        # use geopy geodesic module to get distance in miles and return it to function call
        return geodesic((y_coordinates['lat'], y_coordinates['lng']),
                        (current_location['lat'], current_location['lng'])).miles

    @staticmethod
    def str_to_coordinates(str_coordinates):
        """
        Converts comma separated coordinates to dictionary object of coordinates
        :param str_coordinates: comma separated (no spaces) coordinates in str type
        :return: dictionary {lat:[latitude], 'lng':[longitude]}
        """
        # Ideally method name would be prefixed with __ name mangling rules but is used by
        # main.extend_NITE so this is not possible therefore has to be a public static method ew
        return {'lat': str_coordinates.split(",")[0], 'lng': str_coordinates.split(",")[1]}

    def fetch_valid_venues(self, start_location, radius):
        """

        Uses User's preferences to get all venues which fit our users criteria using custom SQL
        command. Uses mainly arguments from instantiation

        :param start_location: users starting location
        :param radius: total radius the user could travel
        :return: Pandas Dataframe of valid venues that match users preferences
        """
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
            _command = _command + ''' AND entry_price = "no door charge"'''

        # add to base command based on user preferences
        self.cursor_obj.execute(_command, (self.__smartness,))  # execute command

        _fields = ["venue_id", "name", "description", "venue_type",
                   "age_restriction", "entry_price", "dress_code",
                   "dress_rating", "address", "distance"]

        valid_venues_df = pd.DataFrame(columns=_fields)  # create pandas dataframe

        i = 0
        for record in self.cursor_obj.fetchall():
            record = list(record)  # turn record from tuple to list
            record_coordinates = {'lat': record[-1].split(",")[0],
                                  'lng': record[-1].split(",")[1]}
            # get coordinates and split them into a dictionary
            distance = self.__get_distance_between_address(location_coordinates,
                                                           record_coordinates)
            # get distance between address and venues
            if distance <= radius:
                i += 1
                record.append(distance)
                record = pd.DataFrame([record], columns=_fields)
                # turn record into df so it can be appended
                valid_venues_df = valid_venues_df.append(record, ignore_index=True)
                # add series to pandas df
        return valid_venues_df

    def get_vectors(self, vector_ids):
        """
        Gets all vectors from DB using vector IDS

        :param vector_ids: Ids of vectors to get
        :return: vectors in list
        """
        _command = '''SELECT vector FROM venue_vectors WHERE venue_id = ?'''
        # base command for fetching vectors
        _vectors = []  # to collect vectors in temporarily
        for x in vector_ids:
            self.cursor_obj.execute(_command, (x,))  # get vector from db for id
            _vectors.append(self.cursor_obj.fetchall()[0])
            # add new column to valid venues to contain vectors
        return _vectors

    def timings(self, df, num_venues):
        start_time = self.__start.time()
        end_time = self.__end.time()
        duration = self.__end - self.__start
        average_minutes = (duration.seconds / 60) / num_venues
        print('Average Minutes at Venues:', average_minutes)


class create_packages(get_venues):
    """
    Generates package from valid venues
    """

    def __init__(self, kwargs):

        super().__init__(kwargs)
        self.__location = {'lat': kwargs['location'].split(",")[0],
                           'lng': kwargs['location'].split(",")[1]}

        # inherits GetVenues to use when generating create_packages.

    @staticmethod
    def __str_to_vector(vector_str):
        """
        turns string from DB to numpy matrix
        :param vector_str: string of vector. Values space separated
        :return: numpy matrix of (1, 300) of vector
        """
        return np.array([float(x) for x in vector_str.split(' ')]).reshape(1, 300)

    @staticmethod
    def __remove_venue(df, venue_id):
        """
        Removes venue from df

        :param df: a Pandas Dataframe
        :param venue_id: venue id of venue to remove
        :return: adjusted DF
        """
        try:
            index = df[df['venue_id'] == venue_id].index[0]  # get index of venue_to_add
            df = df.drop(index)
            # remove locally from df so that we don't choose the same venue twice
        except IndexError as e:
            # print(venue_id, 'already removed from df')
            pass
        return df

    def desperate_search(self, venue_types, music_types, other_args):
        """
        Searches desperately for a venue if no valid one can be found using the K2K method

        :param venue_types: Type of venues to search for
        :param music_types: Type of music that venues play to search for
        :param other_args: Any further SQL parameters the user may want
        :return: a venue to add to the package
        """
        radius_increase = 0.5
        venue_to_add = None
        while venue_to_add is None:
            print('Entered into DESPERATE MODE!')
            # this only occurs if we cannot find a nightclub in the nearby area
            new_df = self.fetch_valid_venues(self.__location, radius=radius_increase)
            print(len(new_df))
            new_df = new_df.sort_values(by='distance')
            if len(new_df) != 0:
                new_df['vector'] = self.get_vectors(list(new_df['venue_id']))
                venue_to_add = new_df.iloc[0]
                venue_to_add = intensity.check_venue_music_type(venue_to_add,
                                                                self.cursor_obj,
                                                                venue_types,
                                                                music_types,
                                                                new_df, other_args)
                print(venue_to_add)
            radius_increase = radius_increase + 0.5
        return venue_to_add
        # this simply checks to see if we can find any nightclubs near to the user's home location
        # rather than their last venue if we cannot find any clubs near there.
        # we continue doing this until eventually we find a club nearby
        # (this method does not account for users preferences, it just goes into 'desperate
        # mode' and looks for any club)

    @staticmethod
    def __random_choice(df):
        """
        This chooses one of the top five venues randomly. This means that even if the user chooses
        the same NITE options twice, it doesn't necessarily mean they will get the same NITE
        :param df: dataframe of the top x venues by similarity
        :return: a random choice from df
        """
        length = len(df)
        choice = random.randint(0, length-1)
        print(choice)
        return df.iloc[choice]



    def generate_package(self, K2KObj, start_venue, user_vector, df, num_venues):
        """
        Generates the 'package' of the night which refers to every venue that the user should visit
        and in which order.

        :param K2KObj: The K2K object to use, predefined
        :param start_venue: The users starting venue, either set by user or by algo
        :param user_vector: vector to use
        :param df: dataframe of valid venues. Pandas DataFrame
        :param num_venues: number of venues to visit
        :return: package of venues to visit over timespan

        """
        venue_to_add = start_venue
        package = pd.DataFrame(columns=df.columns)

        for venue_number in range(num_venues):
            if venue_number == num_venues - 1:
                print('Last:', len(df))
                venue_to_add = intensity.venue_type(venue_to_add, self.cursor_obj, [1, 11], df)
            elif venue_number == 0:
                print('First: ', len(df))
                venue_to_add = intensity.venue_type(venue_to_add, self.cursor_obj,
                                                    [2, 4, 5, 7, 9], df)

            package = package.append(venue_to_add, ignore_index=True)

            vector = self.__str_to_vector(venue_to_add['vector'][0])
            # get vector of venue_to_add
            composite_vector = K2KObj.composite_vector([user_vector[0], vector[0]])
            # create composite vector of venue to add and user vector to establish what the next
            # vector will be
            location = self.str_to_coordinates(venue_to_add['address'])
            # gets location of venue_to_add

            increase_radius = 0.2
            while increase_radius <= 2:
                df = self.fetch_valid_venues(location, radius=increase_radius)
                if len(df) >= 20:  # TODO: This value is stupid sometimes. Needs to be adjusted
                    break
                increase_radius = increase_radius + 0.2

            # uses location to search for nearby clubs. There must be more than 10 locations
            # within 2 miles we look for clubs within half a mile and increase the step by 0.2
            # if we cannot find enough clubs.
            for venue_id in package['venue_id']:
                df = self.__remove_venue(df, venue_id)
            # removes venues already in the package from the database

            df['vector'] = self.get_vectors(list(df['venue_id']))
            # adds vectors to database
            df = K2KObj.get_closest_vectors(df, composite_vector)
            # sorts database by vectors closest to our composite vector
            self.timings(df, num_venues)
            venue_to_add = self.__random_choice(df.head())
            # defines the next venue as the one with the closest to K2K score (provisionally,
            # we double check this at the start of every loop to ensure the venue has the
            # correct intensity)

        return package
