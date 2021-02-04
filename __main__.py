#!/usr/bin/env python
"""
Main function which calls each module and produces a list of packages to return to user

"""
from time import perf_counter
import pandas as pd
import numpy as np
from nitely_core.cli import cli


class start_NITE:
    def __init__(self, user_obj, my_packages, k2k_obj, radius):
        self.user_obj = user_obj
        self.my_packages = my_packages
        self.k2k_obj = k2k_obj
        self.radius = radius

    @property
    def get_keywords(self):
        return self.user_obj.get_keywords

    @property
    def get_user_vector(self):
        return self.k2k_obj.get_user_vector

    def get_df(self, start_location=None):
        if start_location is not None:
            start_location = self.user_obj.str_to_coordinates(start_location)
        return self.user_obj.fetch_valid_venues(start_location, self.radius)

    def get_vectors(self, venue_ids):
        return self.user_obj.get_vectors(venue_ids)

    def add_similarity(self, df, vector):
        return self.k2k_obj.get_closest_vectors(df, vector)

    def composite_vector(self, vecs):
        return self.k2k_obj.composite_vector(vecs)

    def create_package(self, starting_venue, vector, df, number_of_venues):
        return self.my_packages.generate_package(self.k2k_obj, starting_venue,
                                                 vector, df, number_of_venues)

    @staticmethod
    def drop_used_venues(package, df):
        for venue_id in package['venue_id']:
            # this loop drops all used venues from a df of potential venues
            try:
                index = df[df['venue_id'] == venue_id].index[0]
                df = df.drop(index)
            except IndexError as e:
                print(e)
                print('Record', venue_id, 'already removed!')

        return df


def main(new_nite):
    valid_venues_df = new_nite.get_df(
        start_location='51.4889785,-0.1416508')  # get all valid vectors with distances

    valid_venues_df['vector'] = new_nite.get_vectors(valid_venues_df['venue_id'])
    # added vectors to df

    users_club_ids = [302, 108, 169, 185, 91]  # get users favourite clubs

    _vectors = new_nite.get_vectors(users_club_ids)
    # get each vector for each of users favourite clubs
    for i, __ in enumerate(_vectors):
        _vectors[i] = np.array([float(x) for x in _vectors[i][0].split(' ')]).reshape(1, 300)
        # reshape all vectors into numpy array

    new_vectors = [new_nite.get_user_vector]
    # TODO: seems stupid not to score the keywords. Bit of logic in the website - TESS

    # new_vectors.append(new_nite.composite_vector(_vectors))
    # create composite vector of all users favourite club vectors

    # new_vectors.append(new_nite.composite_vector([new_vectors[0], new_vectors[1]]))
    # create a composite vector of both of the previous vectors

    user_packages = []
    package_columns = list(valid_venues_df.columns)
    package_columns.append('similarity')

    for v in new_vectors:
        df = new_nite.add_similarity(valid_venues_df, v)
        # get df sorted via the vector we are using
        starting_venue = df.iloc[0]  # get top rated venue as starting venue
        new_package = new_nite.create_package(starting_venue, v, df, 3)
        # get the package based on vector
        valid_venues_df = new_nite.drop_used_venues(new_package, df)
        user_packages.append(new_package)  # holds all create_packages

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # print(user_packages)
    print("Action took in seconds:", perf_counter())

    """
    Send user_packages back to website to display here
    this creates 'selected_package'
    """
    return user_packages, new_nite


def extend_NITE(selected_package, current_nite):
    starting_venue = selected_package.iloc[-1]
    user_vector = current_nite.get_user_vector
    valid_venues_df = current_nite.get_df(start_location=starting_venue['address'])
    valid_venues_df['vector'] = current_nite.get_vectors(valid_venues_df['venue_id'])
    df = current_nite.add_similarity(valid_venues_df, user_vector)
    df = current_nite.drop_used_venues(selected_package, df)
    new_package = current_nite.create_package(starting_venue, user_vector,
                                              df, 2)
    return new_package.iloc[-1]


if __name__ == '__main__':
    packages, nite = main(start_NITE(*cli(), radius=4))
    print(packages)
    # new_venue = extend_NITE(packages[0], nite)
    # print(new_venue)
    # user_obj.timings(selected_package)
