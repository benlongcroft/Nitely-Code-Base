import numpy as np


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
        type_to_bin = {'pub': '000', 'bar': '001', 'club': '010', 'other': '011', 'live': '100'}
        self.__id = venue_id
        self.__name = name
        self.__description = description
        self.__location = location
        self.__venue_type = type_to_bin[venue_type.lower()] + str(restaurant) + str(club)
        # takes venue_type, restaurant and club arguments and creates a 5 bit binary code
        # denoting the venue type
        self.__timings = timings
        self.__vector = self.__str_to_vector(vector)
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
        return self.__timings.get_timings()

    @property
    def get_vector(self):
        return self.__vector

    @property
    def get_id(self):
        return self.__id

    def __str_to_vector(self, vector_str):
        """
        turns string from DB to numpy matrix
        :param vector_str: string of vector. Values space separated
        :return: numpy matrix of (1, 300) of vector
        """
        vector_str = vector_str.split(' ')
        vec = ''
        for val in vector_str:
            if val == '':
                continue
            else:
                vec = vec + ' ' + val
        # TODO: Fix this method because its shit
        return np.array([float(x) for x in vec.split(' ')[1:]]).reshape(1, 300)

    def __repr__(self):
        """
        Print string representation of venue object for dev purposes
        :return: string of vector object for printing
        """
        return str(str(self.__id) + ' ' +
                   self.__name + ' ' +
                   self.__venue_type + ' ' +
                   self.__location + ' ' +
                   self.__description + ' ' +
                   str(self.__vector))
