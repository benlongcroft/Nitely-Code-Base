import numpy as np
from Toolbox import str_to_coordinates, db_to_type, str_to_vector

class venue:
    """
    venue object that stores a venue - data should be loaded directly from database into this class
    """

    def __init__(self, venue_id, name, description,
                 location, venue_type, restaurant,
                 club, vector, timings):
        """
        Constructor - converts arguments into valid format for storage in venue class
        :param venue_id: the id of the venue in the database - integer
        :param name: the name of the venue - string
        :param description: the description of the venue which denotes it vector - string
        :param location: the location of the venue - coordinates
        :param venue_type: the type of venue (see type_to_bin) - string
        :param restaurant: whether the venue is a restaurant or not - boolean value (int)
        :param club: whether the venue is a club or not - boolean value (int)
        :param vector: vector of venue from description - string
        :param timings: timings object for venue - contains opening and closing times
        """
        self.__id = venue_id
        self.__name = name
        self.__description = description
        self.__location = str_to_coordinates(location)
        self.__venue_type = db_to_type(venue_type, restaurant, club)
        # takes venue_type, restaurant and club arguments and creates a 5 bit binary code
        # denoting the venue type
        self.__timings = timings
        self.__vector = str_to_vector(vector)
        # converts vector from string to np.matrix (1,300) object

    @property
    def get_name(self):
        return self.__name

    @property
    def get_description(self):
        return self.__description

    @property
    def get_location(self):
        return self.__location

    @property
    def get_venue_type(self):
        return self.__venue_type

    @property
    def get_timings(self):
        return self.__timings

    @property
    def get_vector(self):
        return self.__vector

    @property
    def get_id(self):
        return self.__id

    def __repr__(self):
        """
        Print string representation of venue object for dev purposes
        :return: string of vector object for printing
        """
        return str(str(self.__id) + ' ' +
                   self.__name + ' ' +
                   self.__venue_type + ' ' +
                   str(self.__location) + ' ' +
                   self.__description + ' ' +
                   repr(self.__timings))
