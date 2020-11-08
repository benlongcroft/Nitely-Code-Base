#!/usr/bin/env python

from orfic.cli import cli
from K2K.main import GetClosestVectors, ConvertKeywordsToVectors
import sqlite3

if __name__ == '__main__':
    VenueObj = cli()
    db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
    cursor_obj = db_obj.cursor()
    valid_venues_df = VenueObj.FetchValidVenues(None, cursor_obj)
    vector_df = VenueObj.Get(valid_venues_df, cursor_obj)
    print(vector_df.head())
    # valid_venue_ids = valid_venues_df['venue_id']
