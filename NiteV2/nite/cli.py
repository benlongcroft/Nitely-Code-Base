import argparse
from .VenueVectors import GetVenueVectors

def cli():
    parser = argparse.ArgumentParser(prog="main")
    parser.add_argument("--smartness", help="Smartness of Dress", type=int)
    parser.add_argument("--paid", help="Check for free entry criteria", type=bool)
    parser.add_argument("--date", help="String input of date", type=str)
    parser.add_argument("--TwentyOnePlus", help="Check if user only wants 21+ clubs", type=bool)
    parser.add_argument("--location", help='coordinates seperated by a comma i.e lat,long', type=str)
    parser.add_argument("--location_distance", help="enter distance from location address in miles", type=int)
    args = parser.parse_args()

    criteria = GetVenueVectors(**vars(args))
    AllValidVenues = criteria.GetValidVenues()
