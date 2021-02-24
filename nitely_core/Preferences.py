class preferences:
    def __init__(self, keywords, location, location_distance,
                 magic_words, start_time, end_time):
        self.__keywords = keywords
        self.__location = location
        self.__location_distance = location_distance
        self.__magic_words = magic_words
        self.__start_time = start_time
        self.__end_time = end_time

    def get_keywords(self):
        return self.__keywords

    def get_location(self):
        return self.__location

    def get_location_distance(self):
        return self.__location_distance

    def get_magic_words(self):
        return self.__magic_words

    def get_weightings(self):
        return [1 for x in range(len(self.__keywords))]

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time


