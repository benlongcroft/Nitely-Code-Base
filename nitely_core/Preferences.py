
class preferences:
    """preferences object which holds the users preferences for a specific NITE - when paired with
    a account object it can create a user object via inheritance"""
    def __init__(self, keywords, location, location_distance,
                 magic_words, start_time, end_time):
        """
        Constructor object - saves each parameter as a private attribute
        :param keywords: the keywords of the user - may contain magic words
        :param location: the location of the user - coordinates from start_NITE in dict format
        :param location_distance: total distance the user wants to travel from location
        :param magic_words: all magic words in keywords
        :param start_time: datetime object for start of NITE
        :param end_time: datetime object for end of NITE
        """
        self.__keywords = keywords
        self.__location = location
        self.__location_distance = location_distance
        self.__magic_words = magic_words
        self.__start_time = start_time
        self.__end_time = end_time

    @property
    def get_keywords(self):
        return self.__keywords

    @property
    def get_location(self):
        return self.__location

    @property
    def get_location_distance(self):
        return self.__location_distance

    @property
    def get_magic_words(self):
        return self.__magic_words

    @property
    def get_weightings(self):
        return [1 for x in range(len(self.__keywords))]

    @property
    def get_start_time(self):
        return self.__start_time

    @property
    def get_end_time(self):
        return self.__end_time



