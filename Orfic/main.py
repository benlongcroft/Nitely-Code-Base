#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import sqlite3
import pandas as pd

if __name__ == '__main__':
    UserObj = cli() # Get User object from cli() input
    db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
    cursor_obj = db_obj.cursor() # instantiate a cursor for db
    keywords = UserObj.get_keywords # get keywords for K2K
    valid_venues_df = UserObj.FetchValidVenues(None, cursor_obj) # get all valid vectors with distances
    valid_venues_df = UserObj.Get(valid_venues_df, cursor_obj) # added vectors to df
    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])
    df = K2KObj.get_df
    user_vector = K2KObj.get_user_vector
    # To get closest vectors to a different dataframe now requires you to use the method
    # df = K2KObj.GetClosestVectors(df, user_vector) instead of reinstantiating the object
    df.sort_values(by=['similarity'], inplace=True,
                                ignore_index=True)
    pd.set_option('display.max_columns', None)
    # TODO: sort venues so that you can choose starting venues and then iterate from them to find next locations
    print(df)

# TODO: also look for inheritence/compisition options within these classes