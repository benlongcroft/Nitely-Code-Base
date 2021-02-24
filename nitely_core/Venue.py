import numpy as np


class venue:
    def __init__(self, venue_id, name, description,
                 location, venue_type, restaurant,
                 club, vector, timings):
        type_to_bin = {'pub': '000', 'bar': '001', 'club': '010', 'other': '011', 'live': '100'}
        self.__id = venue_id
        self.__name = name
        self.__description = description
        self.__location = location

        self.__venue_type = type_to_bin[venue_type] + str(restaurant) + str(club)

        self.__timings = timings
        self.__vector = self.__str_to_vector(vector)

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_location(self):
        return self.__location

    def get_venue_type(self):
        return self.__venue_type

    def get_timings(self):
        return self.__timings.get_timings()

    def get_vector(self):
        return self.__vector

    def get_id(self):
        return self.__id

    def __str_to_vector(self, vector_str):
        """
        turns string from DB to numpy matrix
        :param vector_str: string of vector. Values space separated
        :return: numpy matrix of (1, 300) of vector
        """
        return np.array([float(x) for x in vector_str.split(' ')]).reshape(1, 300)
