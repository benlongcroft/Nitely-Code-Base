from nitely_core.cli import cli
from nitely_core import start_NITE
from vector_k2k import K2K
from Playground import VectorVisualiseTSNE
from nitely_core import Venue
import spacy


def main(kwargs):
    """
    Main NITE program - what is called when a new session is to be created for a user
    :param kwargs: commandline input from cli argparser
    :return: NITE's as package objects
    """
    start_venue = None
    # TODO: change the above arguments so they are defined by user
    nite_obj = start_NITE(kwargs)

    user_obj = nite_obj.get_user()
    k2k_obj = K2K(user_obj.get_keywords, user_obj.get_weightings)

    user_vector = user_obj.get_user_vector(k2k_obj)
    venues = nite_obj.get_nearby_venues(user_obj.get_location, user_obj.get_location_distance, [])
    venue_similarity = nite_obj.get_similarity(venues, user_vector)
    p = nite_obj.create_packages(k2k_obj, user_vector, venue_similarity, start_venue)
    print(p)
    print(p.get_types())
    # VectorVisualiseTSNE.main(p, user_vector)
    return p


if __name__ == '__main__':
    packages = main(cli())
