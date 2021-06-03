class query:
    """Query class contains all query information and constructs it"""
    def __init__(self, location, key, price, tag, opennow):
        self.__base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        self.longitude = location['lng']
        self.latitude = location['lat']
        self.__key = key
        self.price = price
        self.tag = tag
        self.opennow = opennow
        query = self.__base + "location="+self.latitude+","+self.longitude
        if self.price is not None:
            query = query + "&price="+self.price

        if self.opennow is not None:
            query = query + "&opennow="+self.opennow

        if self.tag is not None:
            query = query + "&type="+self.tag

        self.__query = query + "&key=" + self.__key + "&rankby=distance"

    def __repr__(self):
        return self.__query

