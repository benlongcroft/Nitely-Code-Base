from Account import account
from Preferences import preferences
from User import user
import sqlite3
from Venue import venue
from Timings import timings
from Package import package
import random
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

    def get_nearby_venues(self, location, radius, types):
        """
        Gets nearby venues to location by type
        :param location: location of user
        :param radius: total radius of distance user is willing to travel to next venue
        :param types: types of venues to fetch
        :return: list of Venue objects
        """
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
            # quick distance check to filter out any too far out results

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
            if db_to_type(venue_data[4], venue_data[5], venue_data[6]) in types or types == []:
                # if type of venue is in types specified by param
                valid_venue_objs.append(venue(venue_data[0], venue_data[1], venue_data[2],
                                              venue_data[3], venue_data[4], venue_data[5],
                                              venue_data[6], venue_data[7],
                                              timings(open_times, close_times)))
        return valid_venue_objs

    @staticmethod
    def get_similarity(venues, u_vector):
        """
        Static method that finds the similarity between a vector and a list of venue objects
        :param venues: a list of venue objects to check - see venue class
        :param u_vector: a numpy vector of size 300 to evaluate against the list of venues
        :return: dictionary of length venues containing the venue object (key)
        and a euclidean distance score
        """
        u_vector = u_vector.reshape(1, 300)
        similarity = {}
        for venue_obj in venues:
            venue_vector = venue_obj.get_vector
            venue_vector = venue_vector.reshape(1, 300)
            # split the string vector and convert to
            # numpy array of floats
            cos = np.linalg.norm((u_vector-venue_vector))
            similarity[venue_obj] = cos
        return sort_dictionary(similarity)

    def get_time_slot(self, new_venue, package_timings):
        """
        Checks that new_venue timings are within the times specified by the user
        :param new_venue: The new venue to check as a Venue object
        :param package_timings: Dictionary of the timings of the venues (venue:timings)
        :return: False if the venue is invalid, otherwise returns timings for new_venue
        """
        v_timings = new_venue.get_timings
        # get venue timings
        start_time = self.__user.get_start_time
        end_time = self.__user.get_end_time
        # get users start and end times
        total_time = (end_time - start_time)
        # find total time the user will spend out
        alpha = (total_time / self.__number_of_venues)
        # Find average time at each venue
        if package_timings != {}:
            # if there are packages already, assign the
            # leaving time of the first venue as the start time
            for key in package_timings.keys():
                value = package_timings[key]
                if value > start_time:
                    start_time = value
            assert isinstance(start_time, object)

        ideal_time = (start_time + alpha)
        # ideal time is the ideal time to leave the venue
        opening_time, closing_time = v_timings.get_day(date_str_to_weekday(self.__date))

        if opening_time == 'CLOSED' or closing_time == 'CLOSED':
            # check venue isn't closed first, if so - return false
            return False

        opening_time, closing_time = convert_to_datetime(opening_time, closing_time, self.__date)
        if closing_time >= ideal_time and start_time >= opening_time:
            # if the ideal time is before the closing time and the start time is after
            # the opening time
            package_timings[new_venue] = ideal_time
        else:
            # if venue is not able to be visited due to opening/closing times, return false
            return False
        return package_timings

    def find_next_venue(self, not_applicable, vector, location, venue_number):
        """
        Finds the next venue to add to the package
        :param vector: The users vector to compare with
        :param location: The current location of the user before the user moves to the next location
        :param not_applicable: Any venues which are invalid for this timestamp or other reasons
        :param venue_number: The number of the venue in the NITE
        :return: The next venue to add to package venues
        """
        if venue_number == 0:
            types = ['00000', '00010', '00110',
                     '00100', '01100', '01101',
                     '01110', '01111', '10010']
            # all possible types for first venue
        elif venue_number == self.__number_of_venues - 1:
            types = ['01001', '01011', '00101',
                     '00111', '10011', '10001',
                     '01101', '01111']
            # all possible types for last venue
        else:
            types = ['00111', '00110', '00101', '00100',
                     '01011', '01010', '01001', '01000',
                     '01111', '01110', '01101', '01100',
                     '10011', '10010', '10001', '10000']
            # all possible types for other venues
        increase_radius = 0.2
        while increase_radius <= 2:
            # Increase radius by 0.2 each time. CAP at 2 miles from location

            new_venues = self.get_nearby_venues(location, increase_radius, types)
            if len(new_venues) >= 20:
                # This means there must be 20 venues nearby to choose from
                # TODO: This value is stupid sometimes. Needs to be adjusted
                break
            increase_radius = increase_radius + 0.2

        valid_venues = delete_duplicates(new_venues, not_applicable)
        # deletes all not applicable venues (those already in package and those already checked)

        similarity_scores = self.get_similarity(valid_venues, vector)
        # gets all venues ranked in similarity

        top_venues = get_head_of_dict(similarity_scores, 3)
        # gets top three venues of correct type (from types param in get_nearby_venues)

        venue_to_add = list(top_venues.keys())[0]
        # This just adds an element of randomness by selecting randomly one of the three best
        # venues
        return venue_to_add

    def create_packages(self, K2K, user_vec, venue_similarity, start_venue):
        """
        Creates a package from the user_obj given venue_similarity

        :param K2K: The K2K object created for the user
        :param user_vec: The users vector
        :param venue_similarity: result of get_similarity method
        - dictionary of {venue_obj:similarity to vector}
        :param start_venue: A venue to start at, if none is defined - will generate automatically
        :return: a package object of the NITE
        """
        package_venues = {}

        location = self.__user_preferences.get_location
        venue_to_add = None
        for venue_number in range(self.__number_of_venues):
            not_applicable = list(package_venues.keys())
            # always define not applicable venues as venues that are already in the package
            # this prevents repeating venues in the NITE
            if (start_venue is None) and (venue_number == 0):
                # if a start venue is not defined by the user...
                top_venues = get_head_of_dict(venue_similarity, 3)
                # get top_venues and choose one at random
                venue_to_add = random.choice(list(top_venues.keys()))
            elif (start_venue is not None) and (venue_number == 0):
                # if start_venue is defined, add the start venue to package venues
                output = self.get_time_slot(start_venue, package_venues)
                if not output:
                    # if start venue is not open at desired time return this
                    return "Start venue is invalid!"
                else:
                    # otherwise, its given a timeslot and added to package venues
                    package_venues = output
            else:
                # if we are not on the first venue, find the next venue
                venue_to_add = self.find_next_venue(not_applicable, user_vec,
                                                    location, venue_number)
                vector = venue_to_add.get_vector
                user_vec = K2K.composite_vector([user_vec, vector])
                # create composite vector of previous club and user_vector to ensure that
                # the NITE 'flows' by making sure we choose similar clubs to the previous venue
                # this is cumulative as user_vec never returns to its initial state defined
                # by only keywords
                location = venue_to_add.get_location
            if venue_to_add is None:
                print('Start venue defined by user')
                continue
            else:
                while True:
                    output = self.get_time_slot(venue_to_add, package_venues)
                    # check if venue is open at given time
                    if not output:
                        not_applicable.append(venue_to_add)
                        # if its not valid, add it to not_applicable and find a new venue
                        venue_to_add = self.find_next_venue(not_applicable, user_vec, location, venue_number)
                    else:
                        package_venues = output
                        break
        print(package_venues)
        return package(package_venues)
