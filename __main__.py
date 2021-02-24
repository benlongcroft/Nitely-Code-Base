from nitely_core.cli import cli
from nitely_core import start_NITE
from vector_k2k import K2K


def main(kwargs):
    nite_obj = start_NITE(kwargs)
    user_obj = nite_obj.get_user()
    keywords = user_obj.get_keywords()
    k2k_obj = K2K(keywords, user_obj.get_weightings())
    user_vector = user_obj.get_user_vector(k2k_obj)
    venues = nite_obj.get_nearby_venues()
    venue_similarity = nite_obj.get_similarity(
        venues)  # TODO: implement this method - return dictionary {venue : similarity}
    nite_obj.create_package(venues, venue_similarity)


if __name__ == '__main__':
    packages = main(cli())
