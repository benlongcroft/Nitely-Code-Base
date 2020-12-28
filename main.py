#!/usr/bin/env python
"""
Main function which calls each module and produces a list of packages to return to user

"""
from time import perf_counter
import pandas as pd
import numpy as np
from orfic.cli import cli
from K2K.main import K2K

if __name__ == '__main__':
    t1_start = perf_counter()

    user_obj, my_package = cli()  # Get User object from cli() input

    keywords = user_obj.get_keywords  # get keywords for K2K

    valid_venues_df = user_obj.fetch_valid_venues(None, 4)  # get all valid vectors with distances

    valid_venues_df['vector'] = user_obj.get_vectors(list(valid_venues_df['venue_id']))
    # added vectors to df

    users_club_ids = [302, 108, 169, 185, 91]  # get users favourite clubs

    _vectors = user_obj.get_vectors(users_club_ids)
    # get each vector for each of users favourite clubs
    for i, __ in enumerate(_vectors):
        _vectors[i] = np.array([float(x) for x in _vectors[i][0].split(' ')]).reshape(1, 300)
        # reshape all vectors into numpy array

    new_vectors = []
    k2k_obj = K2K(keywords, [1 for x in range(len(keywords))])
    new_vectors.append(k2k_obj.composite_vector(_vectors))
    # create composite vector of all users favourite club vectors
    new_vectors.append(k2k_obj.get_user_vector)  # get user vector from keywords

    new_vectors.append(k2k_obj.composite_vector([new_vectors[0], new_vectors[1]]))
    # create a composite vector of both of the previous vectors

    packages = []
    package_columns = list(valid_venues_df.columns)
    package_columns.append('similarity')
    current_package = pd.DataFrame(columns=package_columns)

    for v in new_vectors:
        df = k2k_obj.get_closest_vectors(valid_venues_df, v)
        # get df sorted via the vector we are using
        starting_venue = df.iloc[0]  # get top rated venue as starting venue
        new_package = my_package.generate_package(k2k_obj, starting_venue, v, df, 3)
        # get the package based on vector
        for venue_id in new_package['venue_id']:
            # this loop drops all used venues from the 'master' df of potential venues
            try:
                index = valid_venues_df[valid_venues_df['venue_id'] == venue_id].index[0]
                valid_venues_df = valid_venues_df.drop(index)
            except Exception as exception:

                print(exception)
                print('Record', venue_id, 'already removed!')
        packages.append(new_package)  # holds all create_packages

    print(packages)
    print("Action took in seconds:", perf_counter())

    """
    Send packages back to website to display here
    this creates 'selected_package'
    """

    packages_with_timings = timings.timings(selected_package)
