#!/usr/bin/env python

from nite.cli import cli
import sqlite3

if __name__ == '__main__':
    VenueObj = cli()
    db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
    cursor_obj = db_obj.cursor()
    AllValidVenues = VenueObj.GetValidVenues(None, db_obj, cursor_obj)