from Account import account
from Preferences import preferences
from User import user
import datetime
import sqlite3
from geopy.distance import geodesic
from Venue import venue
from Timings import timings

def str_to_coordinates(str_coordinates):
    """
    Converts comma separated coordinates to dictionary object of coordinates
    :param str_coordinates: comma separated (no spaces) coordinates in str type
    :return: dictionary {lat:[latitude], 'lng':[longitude]}
    """
    return {'lat': str_coordinates.split(",")[0], 'lng': str_coordinates.split(",")[1]}


def convert_to_datetime(start_time, end_time, date):
    try:
        _format_str = '%d%m%Y%H:%M'
        # should be in format DDMMYYYY
        _date_str = date
        start = datetime.datetime.strptime(_date_str + start_time,
                                           _format_str)
        end = datetime.datetime.strptime(_date_str + end_time, _format_str)
        return start, end
        # converts date and time into datetime object

    except Exception as e:
        print('Error when transferring into datetime object')
        print(e)


def get_distance_between_coords(current_location, y_coordinates):
    """
    Gets distance as crow flies between two addresses

    :param current_location: Users current location in coordinates
    :param y_coordinates: location to travel to in coordinates
    :return: Distance in miles between coordinates
    """
    # use geopy geodesic module to get distance in miles and return it to function call
    return geodesic((y_coordinates['lat'], y_coordinates['lng']),
                    (current_location['lat'], current_location['lng'])).miles


class start_NITE:
    def __init__(self, kwargs):
        location = str_to_coordinates(kwargs['location'])
        if kwargs['location_distance'] > 50:
            print("Distance is too far to accurately represent club_data")
            location_distance = 49
        else:
            location_distance = kwargs['location_distance']
        keywords = kwargs['keywords']
        users_magic_words = kwargs['magic_words']
        start_time, end_time = convert_to_datetime(kwargs['start_time'],
                                                   kwargs['end_time'],
                                                   kwargs['date'])
        telephone = kwargs['telephone']
        user_name = kwargs['name']

        self.__user_account = account(user_name, telephone)
        self.__user_preferences = preferences(keywords,
                                              location,
                                              location_distance,
                                              users_magic_words,
                                              start_time,
                                              end_time)
        self.__user = user(self.__user_preferences, self.__user_account)
        self.db_obj = sqlite3.connect(
            '/Users/benlongcroft/Documents/Nitely Project/Nitely/VENUES.db')  # connect to database
        # TODO: move db to accessible location
        self.cursor_obj = self.db_obj.cursor()

    def get_account(self):
        return self.__user_account

    def get_preferences(self):
        return self.__user_preferences

    def get_user(self):
        return self.__user

    def get_nearby_venues(self):
        """
        Uses user to get all venues which fit our users criteria using custom SQL
        command.

        :return: list of venue objects that are valid for use
        """
        location = self.__user.get_location
        radius = self.__user.get_location_distance
        magic_words = self.__user.get_magic_words
        venues = []

        self.cursor_obj.execute('''SELECT id, location FROM venue_info''')

        for record in self.cursor_obj.fetchall():
            record = list(record)  # turn record from tuple to list
            venue_id = record[0]
            record_coordinates = {'lat': record[-1].split(" ")[0],
                                  'lng': record[-1].split(" ")[1]}
            # get coordinates and split them into a dictionary

            distance = get_distance_between_coords(location, record_coordinates)
            # get distance between address and venues

            if distance <= radius:
                venues.append(venue_id)

        valid_venue_objs = []
        for venue_id in venues:
            venue_id = str(venue_id)
            self.cursor_obj.execute('''SELECT id, name, description, location, type, restaurant, 
                                        club, vector FROM venue_info WHERE id = ?''', (venue_id,))
            venue_data = [*(self.cursor_obj.fetchall()[0])]
            self.cursor_obj.execute('''SELECT day, open, close FROM by_week WHERE venue_id = ?''',
                                    (venue_id,))
            timing_data = [*self.cursor_obj.fetchall()]
            open = {}
            close = {}
            for day in timing_data:
                open[day[0]] = day[1]
                close[day[0]] = day[2]

            valid_venue_objs.append(venue(venue_data[0], venue_data[1], venue_data[2],
                                          venue_data[3], venue_data[4], venue_data[5],
                                          venue_data[6], venue_data[7], timings(open, close)))

        # TODO add the timings object to venue instantiation
        return valid_venue_objs

    def get_similarity(self, venues):
        pass

    def create_packages(self, venues, venue_similarity):
        pass
