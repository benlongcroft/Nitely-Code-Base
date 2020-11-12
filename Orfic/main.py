#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import sqlite3
import pandas as pd

if __name__ == '__main__':
    UserObj = cli() # Get User object from cli() input

    # db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
    # cursor_obj = db_obj.cursor() # instantiate a cursor for db
    keywords = UserObj.get_keywords # get keywords for K2K

    valid_venues_df = UserObj.FetchValidVenues(None) # get all valid vectors with distances
    valid_venues_df = UserObj.Get(valid_venues_df) # added vectors to df

    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])
    df = K2KObj.get_df
    user_vector = K2KObj.get_user_vector

    packages = []

    for i in range(4):
        row = df.iloc[0]
        current_package = pd.DataFrame(columns = df.columns)
        current_package, df = UserObj.GetNextVenue(K2KObj, row, user_vector, df, current_package, 3, 1)
        packages.append(current_package)
        # print(df)
    print(packages)

# TODO: also look for inheritence/compisition options within these classes