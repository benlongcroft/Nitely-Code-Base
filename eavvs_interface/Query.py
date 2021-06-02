
class query:
    def __init__(self, location, key, price, tag, opennow):
        self.__base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        self.longitude = location['lng']
        self.latitude = location['lat']
        self.__key = key
        self.price = str(price)
        self.tag = tag
        self.opennow = str(opennow).lower()

    def get_query(self):
        query = self.__base + "location="+self.longitude+","+self.latitude
        if self.price is not None:
            query = query + "&price="+self.price

        if self.opennow is not None:
            query = query + "&opennow="+self.opennow

        if self.tag is not None:
            query = query + "&type="+self.tag

        query = query + "&key=" + self.__key + "&rankby=distance"
        return query

