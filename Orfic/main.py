#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import pandas as pd
import numpy as np

if __name__ == '__main__':
    UserObj = cli()  # Get User object from cli() input

    keywords = UserObj.get_keywords  # get keywords for K2K

    valid_venues_df = UserObj.FetchValidVenues(None, 4)  # get all valid vectors with distances

    valid_venues_df['vector'] = UserObj.GetVectors(list(valid_venues_df['venue_id']))  # added vectors to df

    users_club_ids = [302, 108, 169, 185, 91]

    _vectors = UserObj.GetVectors(users_club_ids)
    for i in range(len(_vectors)):
        _vectors[i] = np.array([float(x) for x in _vectors[i][0].split(' ')]).reshape(1, 300)

    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])
    composite_vector = K2KObj.CompositeVector(_vectors)
    df = K2KObj.get_df
    user_vector = K2KObj.get_user_vector

    user_vector = K2KObj.CompositeVector([composite_vector, user_vector])
    packages = []

    current_package = pd.DataFrame(columns=df.columns)

    starting_venue = df.iloc[0]

    current_package = UserObj.GetNextVenue(K2KObj, starting_venue, user_vector, df, 3)
    packages.append(current_package)
    print(packages)