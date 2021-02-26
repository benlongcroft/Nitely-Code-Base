"""
    Commandline arguments which can be called by script to execute orfic session if message is
    received from front end management service
"""

import argparse


def cli():
    """
    Commandline arguments which can be called by script to execute NITE session if message is
    received from front end management service
    """

    parser = argparse.ArgumentParser(prog="main")

    parser.add_argument("--date",
                        help="String input of date",
                        type=str)

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

    parser.add_argument("--magic_words",
                        help="Users magic words",
                        nargs="+",
                        type=str)

    parser.add_argument("--start_time",
                        help="String input of start time",
                        type=str)

    parser.add_argument("--end_time",
                        help="String input of end time",
                        type=str)

    parser.add_argument("--telephone",
                        help="Users telephone",
                        type=str)

    parser.add_argument("--name",
                        help="Users name",
                        type=str)

    args = parser.parse_args()
    args = vars(args)
    print(args)
    return args
