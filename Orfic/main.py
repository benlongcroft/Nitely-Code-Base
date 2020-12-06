#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import pandas as pd
import numpy as np

def get_package(K2KObj, starting_venue, vector, df, num):
    return UserObj.GetNextVenue(K2KObj, starting_venue, vector, df, num)

if __name__ == '__main__':
    UserObj = cli()  # Get User object from cli() input

    keywords = UserObj.get_keywords  # get keywords for K2K

    valid_venues_df = UserObj.FetchValidVenues(None, 4)  # get all valid vectors with distances

    valid_venues_df['vector'] = UserObj.GetVectors(list(valid_venues_df['venue_id']))  # added vectors to df

    users_club_ids = [302, 108, 169, 185, 91] # get users favourite clubs

    _vectors = UserObj.GetVectors(users_club_ids) # get each vector for each of users favourite clubs
    for i in range(len(_vectors)):
        _vectors[i] = np.array([float(x) for x in _vectors[i][0].split(' ')]).reshape(1, 300)
        # reshape all vectors into numpy array

    new_vectors = []
    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])
    new_vectors.append(K2KObj.CompositeVector(_vectors))
    # create composite vector of all users favourite club vectors
    new_vectors.append(K2KObj.get_user_vector) # get user vector from keywords

    new_vectors.append(K2KObj.CompositeVector([new_vectors[0], new_vectors[1]]))
    # create a composite vector of both of the previous vectors

    packages = []

    package_columns = list(valid_venues_df.columns)
    package_columns.append('similarity')
    current_package = pd.DataFrame(columns=package_columns)

    for v in new_vectors:
        df = K2KObj.GetClosestVectors(valid_venues_df, v) #get df sorted via the vector we are using
        starting_venue = df.iloc[0] # get top rated venue as starting venue
        new_package = get_package(K2KObj, starting_venue, v, df, 3) # get the package based on vector
        for id in new_package['venue_id']: # this loop drops all used venues from the 'master' df of potential venues
            try:
                index = valid_venues_df[valid_venues_df['venue_id'] == id].index[0]
                valid_venues_df = valid_venues_df.drop(index)
            except Exception as e:
                print(e)
                print('Record', id, 'already removed!')

        packages.append(new_package) #holds all packages
    print(packages)