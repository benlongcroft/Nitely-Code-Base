"""
    Commandline arguments which can be called by script to execute orfic session if message is
    received from front end management service
"""

import argparse
from .user_preferences import get_venues, create_packages


def cli():

    """
    Commandline arguments which can be called by script to execute orfic session if message is
    received from front end management service
    """

    parser = argparse.ArgumentParser(prog="main")
    parser.add_argument("--smartness",
                        help="Smartness of Dress",
                        type=int)

    parser.add_argument("--paid",
                        help="Check for free entry criteria",
                        action="store_true")

    parser.add_argument("--date",
                        help="String input of date",
                        type=str)

    parser.add_argument("--eighteen",
                        help="Check if user only wants 18+ clubs",
                        action="store_true")

    parser.add_argument("--location",
                        help='coordinates separated by a comma i.e lat,long',
                        type=str)

    parser.add_argument("--location_distance",
                        help="enter distance from location address in miles",
                        type=int)

    parser.add_argument("--keywords",
                        help="All user keywords",
                        nargs='+',
                        type=str)

    parser.add_argument("--gay",
                        help="Determine if user wants to remove gay clubs",
                        action="store_true")

    parser.add_argument("--start_time",
                        help="String input of start time",
                        type=str)

    parser.add_argument("--end_time",
                        help="String input of end time",
                        type=str)

    args = parser.parse_args()

    return get_venues(**vars(args)), create_packages(**vars(args))
