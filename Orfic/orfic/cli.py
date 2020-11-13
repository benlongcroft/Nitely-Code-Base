import argparse
from .UserPreferences import GetVenueVectors


def cli():
    parser = argparse.ArgumentParser(prog="main")
    parser.add_argument("--smartness", help="Smartness of Dress", type=int)
    parser.add_argument("--paid", help="Check for free entry criteria", action="store_true")
    parser.add_argument("--date", help="String input of date", type=str)
    parser.add_argument("--eighteen", help="Check if user only wants 18+ clubs", action="store_true")
    parser.add_argument("--location", help='coordinates separated by a comma i.e lat,long', type=str)
    parser.add_argument("--location_distance", help="enter distance from location address in miles", type=int)
    parser.add_argument("--keywords", help="All user keywords", nargs='+', type=str)
    args = parser.parse_args()
    '''Commandline arguments which can be called by script to execute orfic session if message is received from front 
    end management service '''

    return GetVenueVectors(**vars(args))
