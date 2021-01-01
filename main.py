#!/usr/bin/env python
"""
Main function which calls each module and produces a list of packages to return to user

"""
from time import perf_counter
import pandas as pd
import numpy as np
from nitely.cli import cli


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
    def get_df(self):
        return self.user_obj.fetch_valid_venues(None, self.radius)

    @property
    def get_user_vector(self):
        return self.k2k_obj.get_user_vector

    def get_vectors(self, venue_ids):
        return self.user_obj.get_vectors(venue_ids)

    def add_similarity(self, df, vector):
        return self.k2k_obj.get_closest_vectors(df, vector)

    def composite_vector(self, vecs):
        return self.k2k_obj.composite_vector(vecs)

    def create_package(self, starting_venue, vector, df, number_of_venues):
        return self.my_packages.generate_package(self.k2k_obj, starting_venue,
                                                vector, df, number_of_venues)

def main(new_nite):
    t1_start = perf_counter()

    keywords = new_nite.get_keywords  # get keywords for K2K

    valid_venues_df = new_nite.get_df  # get all valid vectors with distances

    valid_venues_df['vector'] = new_nite.get_vectors(valid_venues_df['venue_id'])
    # added vectors to df

    users_club_ids = [302, 108, 169, 185, 91]  # get users favourite clubs

    _vectors = new_nite.get_vectors(users_club_ids)
    # get each vector for each of users favourite clubs
    for i, __ in enumerate(_vectors):
        _vectors[i] = np.array([float(x) for x in _vectors[i][0].split(' ')]).reshape(1, 300)
        # reshape all vectors into numpy array

    new_vectors = []
    # TODO: seems stupid not to score the keywords. Bit of logic in the website - TESS

    # new_vectors.append(new_nite.composite_vector(_vectors))
    # create composite vector of all users favourite club vectors
    new_vectors.append(new_nite.get_user_vector)  # get user vector from keywords

    # new_vectors.append(new_nite.composite_vector([new_vectors[0], new_vectors[1]]))
    # create a composite vector of both of the previous vectors

    packages = []
    package_columns = list(valid_venues_df.columns)
    package_columns.append('similarity')
    current_package = pd.DataFrame(columns=package_columns)

    for v in new_vectors:
        df = new_nite.add_similarity(valid_venues_df, v)
        # get df sorted via the vector we are using
        starting_venue = df.iloc[0]  # get top rated venue as starting venue
        new_package = new_nite.create_package(starting_venue, v, df, 3)
        # get the package based on vector
        for venue_id in new_package['venue_id']:
            # this loop drops all used venues from the 'master' df of potential venues
            try:
                index = valid_venues_df[valid_venues_df['venue_id'] == venue_id].index[0]
                valid_venues_df = valid_venues_df.drop(index)
            except IndexError as exception:
                print('Record', venue_id, 'already removed!')
        packages.append(new_package)  # holds all create_packages

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(packages)
    print("Action took in seconds:", perf_counter())

    """
    Send packages back to website to display here
    this creates 'selected_package'
    """
    return packages


if __name__ == '__main__':
    packages = main(start_NITE(*cli(), radius=4))
    # user_obj.timings(selected_package)
