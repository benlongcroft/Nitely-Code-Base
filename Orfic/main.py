#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import K2K
# TODO: fix this shit
import sqlite3

if __name__ == '__main__':
    UserObj = cli() # Get User object from cli() input
    db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
    cursor_obj = db_obj.cursor() # instantiate a cursor for db
    keywords = UserObj.keywords # get keywords for K2K
    valid_venues_df = UserObj.FetchValidVenues(None, cursor_obj) # get all valid vectors with distances
    valid_venues_df = UserObj.Get(valid_venues_df, cursor_obj) # added vectors to df
    K2KObj = K2K(valid_venues_df, keywords, [1 for x in range(len(keywords))])

#TODO: also look for inheritence/compisition options within these classes