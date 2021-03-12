class package:
    def __init__(self, list_of_venues):
        self.__names = []
        self.__locations = []
        self.__types = []
        self.__list_of_venues = list_of_venues
        for v in list_of_venues:
            self.__types.append(v.get_venue_type)
            self.__names.append(v.get_name)
            self.__locations.append(v.get_location)

    def get_names(self):
        return self.__names

    def get_locations(self):
        return self.__locations

    def get_types(self):
        return self.__types

    def get_list(self):
        return self.__list_of_venues

    def __repr__(self):
        return str(self.__names)
