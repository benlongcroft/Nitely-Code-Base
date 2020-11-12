#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import sqlite3
import pandas as pd

if __name__ == '__main__':
    UserObj = cli() # Get User object from cli() input

    keywords = UserObj.get_keywords # get keywords for K2K

    valid_venues_df = UserObj.FetchValidVenues(None, 4) # get all valid vectors with distances
    valid_venues_df = UserObj.Get(valid_venues_df) # added vectors to df

    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])
    df = K2KObj.get_df
    user_vector = K2KObj.get_user_vector

    packages = []

    current_package = pd.DataFrame(columns = df.columns)

    starting_venue = df.iloc[0]

    current_package = UserObj.GetNextVenue(K2KObj, starting_venue, user_vector, df, current_package, 3, 0)
    packages.append(current_package)
    print(packages)

# TODO: also look for inheritence/compisition options within these classes