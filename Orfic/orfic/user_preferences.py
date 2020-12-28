"""
Deals with the user inputs and preferences and fetching venues that match the 'hard' criteria.
Calls K2K when necessary. Gets venue vectors, valid dataframes and returns create_packages

"""
import sqlite3
import datetime
from geopy.distance import geodesic
import pandas as pd
import numpy as np
from . import intensity


class get_venues:
    """Gets all valid venues K2K can use based on their preferences"""
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
            self.__location_coordinates = location.split(',')
        except Exception as exception:
            print('Error splitting coordinates')
            print(exception)

        if (smartness <= 5) or (smartness >= 1):
            self.__smartness = smartness
        else:
            print('Smartness value is not within valid range')

        try:
            _format_str = '%d%m%Y'
            # should be in format DDMMYYYY
            _date_str = date
            _datetime_obj = datetime.datetime.strptime(_date_str, _format_str)
            # converts date into datetime object
            self.__date = _datetime_obj.date()
        except Exception as e:
            print('Error when transferring into datetime object')
            print(e)

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
            _command = _command + ''' AND entry_price = no door charge'''

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


class create_packages(get_venues):
    """
    Generates package from valid venues
    """
    def __init__(self, smartness, paid, date,
                 eighteen, location, location_distance,
                 keywords, gay):

        super().__init__(smartness, paid, date,
                         eighteen, location, location_distance,
                         keywords, gay)
        # inherits GetVenues to use when generating create_packages.

    @staticmethod
    def __str_to_vector(vector_str):
        """

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
        except IndexError:
            print(venue_id, 'already removed from df')
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
        while venue_to_add.all() is None:
            print('Entered into DESPERATE MODE!')
            # this only occurs if we cannot find a nightclub in the nearby area
            new_df = self.fetch_valid_venues(self.__location, radius=radius_increase)
            new_df['vector'] = self.get_vectors(list(new_df['venue_id']))
            venue_to_add = intensity.check_venue_music_type(venue_to_add,
                                                            self.cursor_obj,
                                                            venue_types,
                                                            music_types,
                                                            new_df, other_args)
            radius_increase = radius_increase + 0.5
        return venue_to_add
        # this simply checks to see if we can find any nightclubs near to the user's home location
        # rather than their last venue if we cannot find any clubs near there.
        # we continue doing this until eventually we find a club nearby
        # (this method does not account for users preferences, it just goes into 'desperate
        # mode' and looks for any club)

    def check_intensity(self, df, venue_to_add, venue_number, num_venues):
        """
        Checks whether the venue to add to the package is the correct level of 'intensity' for
        its position in the night.

        :param df: all valid venues by users preferences. Pandas DataFrame
        :param venue_to_add: venue to add to package
        :param venue_number: the position of the venue in the night
        :param num_venues: the number of venues visited overall
        :return: the correct venue to add to the package
        """
        _supposed_intensity = venue_number + 1 / num_venues
        last_venue_types = [1, 11]
        last_venue_music = [4, 7, 8, 9, 10, 11, 12, 14, 16, 19, 20, 21]

        first_venue_types = [2, 4, 5, 7, 9]
        first_venue_music = [1, 2, 3, 5, 6, 13, 15, 17, 18]

        # work out how intense the venue should be
        # where 0 is the least intense and 1 is the most intense
        if venue_number == (num_venues - 1):  # if the venue is the last venue in the night
            venue_to_add = intensity.check_venue_music_type(venue_to_add,
                                                            self.cursor_obj,
                                                            last_venue_types,
                                                            last_venue_music,
                                                            df, None)
            if venue_to_add.all() is None:
                venue_to_add = self.desperate_search(last_venue_types, last_venue_music, None)
            # this simply ensures the music type and venue type of the last venue in the package
            # are nightclubs with lively music

        elif venue_number == 0:  # if the venue is the first venue in the night
            other_args = '''AND venues.entry_price = "no door charge"'''
            venue_to_add = intensity.check_venue_music_type(venue_to_add, self.cursor_obj,
                                                            first_venue_types,
                                                            first_venue_music,
                                                            df, other_args)
            if venue_to_add.all() is None:
                venue_to_add = self.desperate_search(first_venue_types,
                                                     first_venue_music,
                                                     other_args)
            # this simply ensures the music type and venue type of the last venue in
            # the package are nightclubs with lively music
        else:
            pass
            # TODO: Need to put in some kind of intensity routine here.
            # Currently not worrying about it. Moving on...

        return venue_to_add

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
            correct_venue = self.check_intensity(df, venue_to_add, venue_number, num_venues)
            venue_to_add = correct_venue
            # if correct_venue and venue_to_add are the same this will do nothing
            package = package.append(venue_to_add, ignore_index=True)

            vector = self.__str_to_vector(venue_to_add['vector'][0])
            # get vector of venue_to_add
            composite_vector = K2KObj.composite_vector([user_vector, vector])
            # create composite vector of venue to add and user vector to establish what the next
            # vector will be
            location = {'lat': venue_to_add['address'].split(",")[0],
                        'lng': venue_to_add['address'].split(",")[1]}
            # gets location of venue_to_add

            increase_radius = 0.2
            while increase_radius <= 2:
                df = self.fetch_valid_venues(location, radius=increase_radius)
                if len(df) >= 10:
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
            venue_to_add = df.iloc[0]
            # defines the next venue as the one with the closest to K2K score (provisionally,
            # we double check this at the start of every loop to ensure the venue has the
            # correct intensity

        return package

    def timings(self, packages, start_time, duration):

