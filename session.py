from nitely_core.cli import cli
from nitely_core import start_NITE
from vector_k2k import K2K
from eavss_connect import connect
from nitely_core.Toolbox import *
from nitely_core.Timings import timings
import sqlite3


class new_session:
    def __init__(self, kwargs):
        """
        Main NITE program - what is called when a new session is to be created for a user
        :param kwargs: commandline input from cli argparser (for now)
        """
        print('------------------------------------------------------')
        print('|  NEW SESSION CREATED -> STARTING SET UP TASKS...   |')
        print('------------------------------------------------------')
        print("Attempting to connect to database")
        db_obj = sqlite3.connect(
            'DB_PATH')
        self.nite_obj = start_NITE(kwargs, db_obj)
        self.user_obj = self.nite_obj.get_user()
        self.k2k_obj = K2K(self.user_obj.get_keywords, self.user_obj.get_weightings)
        self.eavss_obj = connect(db_obj)
        print('------------------------------------------------------')
        print("|                SET-UP TASKS COMPLETE               |")
        print('------------------------------------------------------')
        print("\n")

    def get_event(self, user_vector):
        package = []
        location = self.user_obj.get_location



        return package, user_vector

    def get_context(self, package_venues, user_vector):
        start_time = self.user_obj.get_start_time
        end_time = self.user_obj.get_end_time
        not_applicable = []
        venue_number = 0
        max_requests = 10
        location = self.user_obj.get_location
        for ven in package_venues:
            if ven is not None:
                venue_number += 1
                continue

            venues = self.nite_obj.get_nearby_venues(self.eavss_obj, location,
                                                     venue_number)
            venue_vectors = self.eavss_obj.get_EAVSS_vectors(venues)
            venue_similarity = self.nite_obj.get_similarity(venue_vectors, user_vector)
            r = 0
            for venue_obj in venue_similarity.keys():
                maps_id = venue_obj.get_id
                if max_requests == r:
                    print("Too many requests!")
                    print("Failed due to costs constraint")
                    venue_to_add = None
                    start_time = None
                    end_time = None
                    break
                if venue_obj.get_distance_appeal < 0.001:
                    print(venue_obj.get_name + " is too far away by this method of transport")
                    r += 1
                    print("Skipping...\n")
                    continue

                time_data = self.eavss_obj.get_timings_from_api(maps_id)
                if time_data == 0:
                    r += 1
                    print(venue_obj.get_name + " does not have opening hours listed")
                    print("Skipping...\n")
                    continue

                opening, closing = api_to_timings(time_data['periods'])
                venue_obj.set_timings(timings(opening, closing))
                output = self.nite_obj.get_time_slot(venue_obj, start_time, end_time,
                                                     self.eavss_obj)
                # check if venue is open at given time
                if not output:
                    not_applicable.append(venue_obj)
                    r += 1
                else:
                    start_time = output[0]
                    end_time = output[0]
                    venue_to_add = venue_obj
                    break

            package_venues[venue_number] = [venue_to_add.get_id, [start_time, end_time]]
            location = venue_to_add.get_location
            venue_number += 1
            vector = venue_to_add.get_vector
            user_vector = K2K.composite_vector([user_vector, vector])
        return package_venues

    def build(self):
        """builds the packages in the new session
        :return p: the packages for the user"""
        user_vector = self.user_obj.get_user_vector(self.k2k_obj)
        p, user_vector = self.get_event(user_vector)
        p = self.get_context(p, user_vector)
        return p


# TODO: add new distance happiness to K2K similarity to get_similarity
# TODO: implement access to venue vectors from EAVVS crawler (may be separately networked)
# TODO: Alter create packages to use new venue object
packages = new_session(cli()).build()
