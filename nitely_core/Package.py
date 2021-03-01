from Venue import venue


class package(venue):
    def __init__(self, list_of_venues):
        self.__names = []
        self.__locations = []
        self.__types = []
        for v in list_of_venues:
            self.__types.append(v.get_venue_type)
            self.__names.append(v.get_name)
            self.__locations.append(v.get_location)

    def __repr__(self):
        return str(self.__names)
