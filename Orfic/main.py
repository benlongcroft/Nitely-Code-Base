#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
import sqlite3
import pandas as pd
import numpy as np

def RemoveVenue(df, venue_id):
    index = df[df['venue_id'] == venue_id].index[0]  # get index of venue_to_add
    df = df.drop(index)  # remove locally from df so that we don't choose the same venue twice
    return df

def GetNextVenue(K2KObj, venue_to_add, user_vector, v_df, package, num_venues, n):
    n = n + 1
    if n >= num_venues:
        return package, v_df
    else:
        vector = np.array([float(x) for x in venue_to_add['vector'][0].split(' ')]).reshape(1, 300)  # get venues vector
        composite_vector = K2KObj.CompositeVector(user_vector, vector)
        # find midpoint between users vector and venues vector
        v_df = K2KObj.GetClosestVectors(v_df, composite_vector)
        v_df = v_df.rename_axis(None)
        next_venue = v_df.iloc[0]
        v_df = RemoveVenue(v_df, next_venue['venue_id'])
        package = package.append(next_venue, ignore_index=True)
        return GetNextVenue(K2KObj, next_venue, user_vector, v_df, package, num_venues, n)



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
    # pd.set_option('display.max_rows', None)

    # TODO: sort venues so that you can choose starting venues and then iterate from them to find next locations
    top_venues = df.head(4)

    for index, row in top_venues.iterrows():
        df = RemoveVenue(df, row['venue_id'])

    packages = []

    for index, row in top_venues.iterrows():
        current_package = pd.DataFrame(columns = df.columns)
        current_package = current_package.append(row, ignore_index=True)
        current_package, df = GetNextVenue(K2KObj, row, user_vector, df, current_package, 3, 0)
        packages.append(current_package)
    print(packages)

# TODO: also look for inheritence/compisition options within these classes