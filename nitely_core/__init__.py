from Account import account
from Preferences import preferences
from User import user
import sqlite3
from Venue import venue
from Timings import timings
from Package import package
from scipy.spatial import distance
from Toolbox import *


class start_NITE:
    """
    start_NITE creates a new session from the arguments given on command line
    """

    def __init__(self, kwargs):
        """
        Constructor converts kwargs to valid formats and connects to database
        :param kwargs: command line arguments
        """
        users_location = str_to_coordinates(kwargs['location'])
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
        self.__date = kwargs['date']
        telephone = kwargs['telephone']
        user_name = kwargs['name']
        self.__number_of_venues = kwargs["num_venues"]
        self.__user_account = account(user_name, telephone)
        # creates account object for user
        self.__user_preferences = preferences(keywords,
                                              users_location,
                                              location_distance,
                                              users_magic_words,
                                              start_time,
                                              end_time)
        # creates preferences object for user
        self.__user = user(self.__user_preferences, self.__user_account)
        # passes account and preferences object to user object - user object will inherit all
        # methods and attributes
        self.db_obj = sqlite3.connect(
            '/Users/benlongcroft/Documents/Nitely Project/Nitely/VENUES.db')
        # connect to database
        self.cursor_obj = self.db_obj.cursor()

    def get_account(self):
        return self.__user_account

    def get_preferences(self):
        return self.__user_preferences

    def get_user(self):
        return self.__user

    def get_nearby_venues(self, location, radius):
        """
        Uses user object to get all venues which fit our users criteria using custom SQL
        command.

        :return: list of venue objects that are valid for use
        """
        magic_words = self.__user.get_magic_words
        # TODO: Implement magic word functionality to filter results better
        venues = []
        self.cursor_obj.execute('''SELECT id, location FROM venue_info''')

        for record in self.cursor_obj.fetchall():
            record = list(record)  # turn record from tuple to list
            venue_id = record[0]
            record_coordinates = str_to_coordinates(record[-1])
            # get coordinates and split them into a dictionary

            _distance = get_distance_between_coords(location, record_coordinates)
            # get distance between address and venues

            if _distance <= radius:
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
            open_times = {}
            close_times = {}
            for day in timing_data:
                open_times[day[0]] = day[1]
                close_times[day[0]] = day[2]
            if venue_data[4] is None:
                continue
            valid_venue_objs.append(venue(venue_data[0], venue_data[1], venue_data[2],
                                          venue_data[3], venue_data[4], venue_data[5],
                                          venue_data[6], venue_data[7],
                                          timings(open_times, close_times)))
        return valid_venue_objs

    @staticmethod
    def get_similarity(venues, vector):
        """
        Static method that finds the similarity between a vector and a list of venue objects
        :param venues: a list of venue objects to check - see venue class
        :param vector: a numpy vector of size 300 to evaluate against the list of venues
        :return: dictionary of length venues containing the venue object (key)
        and a euclidean distance score
        """
        vector = vector.reshape(1, 300)
        similarity = {}
        for venue_obj in venues:
            venue_vector = venue_obj.get_vector
            venue_vector = venue_vector.reshape(1, 300)
            # split the string vector and convert to
            # numpy array of floats
            cos = distance.euclidean(vector, venue_vector)
            similarity[venue_obj] = cos
        return sort_dictionary(similarity)

    def get_time_slot(self, new_venue, package_timings):
        v_timings = new_venue.get_timings
        # get venue timings
        start_time = self.__user.get_start_time
        end_time = self.__user.get_end_time
        if start_time == 'CLOSED':
            return False
        # get users start and end times
        total_time = (end_time - start_time)
        # find total time the user will spend out
        alpha = (total_time / self.__number_of_venues)
        # Find average time at each venue
        # start_time = start_time
        if package_timings != {}:
            top_time = start_time
            for key in package_timings.keys():
                value = package_timings[key]
                if value > top_time:
                    top_time = value
            assert isinstance(top_time, object)
            start_time = top_time
        ideal_time = (start_time + alpha)
        opening_time, closing_time = v_timings.get_day(date_str_to_weekday(self.__date))
        opening_time, closing_time = convert_to_datetime(opening_time, closing_time, self.__date)
        # opening_time = datetime.datetime.strptime(opening_time, "%H:%M")
        # closing_time = datetime.datetime.strptime(closing_time, "%H:%M")
        if closing_time >= ideal_time and start_time >= opening_time:
            package_timings[new_venue] = ideal_time
        else:
            return False
        return package_timings

    def find_next_venue(self, package_venues, vector, location, not_applicable):
        increase_radius = 0.2
        while increase_radius <= 2:
            # Increase radius by 0.2 each time. CAP at 2 miles from location
            new_venues = self.get_nearby_venues(location, radius=increase_radius)
            if len(new_venues) >= 20:
                # This means there must be 20 venues nearby to choose from
                # TODO: This value is stupid sometimes. Needs to be adjusted
                break
            increase_radius = increase_radius + 0.2

        valid_venues = delete_duplicates(new_venues, package_venues)
        if not_applicable is not None:
            valid_venues = delete_duplicates(new_venues, not_applicable)

        similarity_scores = self.get_similarity(valid_venues, vector)
        top_venues = get_head_of_dict(similarity_scores, 3)
        venue_to_add = random.choice((list(top_venues.keys())))
        return venue_to_add

    def check_validity(self, venue_to_add, package_timings):
        output = self.get_time_slot(venue_to_add, package_timings)
        if not output:
            return False
        else:
            return True
        # TODO: Fixing below requires this to have intensity added

    def create_packages(self, K2K, user_obj, venue_similarity, start_venue):
        """
        Creates a package from the user_obj given venue_similarity

        :param K2K: The K2K object created for the user
        :param user_obj: The users object
        :param venue_similarity: result of get_similarity method
        - dictionary of {venue_obj:similarity to vector}
        :param start_venue: A venue to start at, if none is defined - will generate automatically
        :return: a package object of the NITE
        """
        package_venues = []
        package_timings = {}
        user_vec = user_obj.get_user_vector(K2K)
        location = self.__user_preferences.get_location
        if start_venue is None:
            top_venues = get_head_of_dict(venue_similarity, 3)
            start_venue = random.choice(list(top_venues.keys()))
        venue_to_add = start_venue
        for venue_number in range(self.__number_of_venues):
            not_applicable = []
            print("VENUE NUMBER:", venue_number)
            print("START VENUE:", venue_to_add.get_name)
            while not self.check_validity(venue_to_add, package_timings):
                not_applicable.append(venue_to_add)
                venue_to_add = self.find_next_venue(package_venues, user_vec, location, not_applicable)
                print("CHOSEN INSTEAD:", venue_to_add.get_name)
                print("CURRENT DAY:", date_str_to_weekday(self.__date))
                print("VENUE TIMES:", venue_to_add.get_timings)
            package_venues.append(venue_to_add)
            print("ADDED", venue_to_add.get_name, "TO PACKAGE VENUES\n")
            vector = venue_to_add.get_vector
            user_vec = K2K.composite_vector([user_obj.get_user_vector(K2K), vector])
            location = venue_to_add.get_location
            venue_to_add = self.find_next_venue(package_venues, user_vec, location, None)
        print(package_venues)
        return package(package_venues, package_timings)
