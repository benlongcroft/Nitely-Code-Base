
class venue:
    """
    venue object that stores a venue - data should be loaded directly from database into this class
    """

    def __init__(self, venue_id, name, location, tags,
                 distance_appeal, timings, price_level, user_rating):
        """
        Constructor - converts arguments into valid format for storage in venue class
        :param venue_id: the id of the venue in the database - integer
        :param name: the name of the venue - string
        :param location: the location of the venue - coordinates
        :param tags: the google API tags for the venue
        :param distance_appeal: the appeal by distance for the user
        :param timings: timings object for venue - contains opening and closing times
        :param price_level: the price level (0-4) of the venue
        :param user_rating: the average user rating of the venue
        """
        self.__id = venue_id
        self.__name = name
        self.__location = location
        self.__tags = tags
        self.__distance_appeal = distance_appeal
        self.__timings = timings
        self.__price_level = price_level
        self.__user_rating = user_rating

    @property
    def get_name(self):
        return self.__name

    @property
    def get_location(self):
        return self.__location

    @property
    def get_tags(self):
        return self.__tags

    @property
    def get_price_level(self):
        return self.__price_level

    @property
    def get_user_rating(self):
        return self.__user_rating

    @property
    def get_timings(self):
        return self.__timings

    @property
    def get_distance_appeal(self):
        return self.__distance_appeal

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
                   str(self.__location) + ' ' +
                   str(self.__distance_appeal) + ' ' +
                   str(self.__price_level) + ' ' +
                   str(self.__user_rating) + ' ' +
                   repr(self.__timings))
