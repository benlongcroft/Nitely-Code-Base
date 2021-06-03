from nitely_core.cli import cli
from nitely_core import start_NITE
from vector_k2k import K2K
from eavss_interface import connect

class new_session:
    def __init__(self, kwargs):
        """
        Main NITE program - what is called when a new session is to be created for a user
        :param kwargs: commandline input from cli argparser (for now)
        """

        # TODO: change the above arguments so they are defined by user
        self.nite_obj = start_NITE(kwargs)
        self.user_obj = self.nite_obj.get_user()
        self.k2k_obj = K2K(self.user_obj.get_keywords, self.user_obj.get_weightings)
        self.eavvs_obj = connect(self.user_obj.get_location)
        self.build()

    def build(self):
        """builds the packages in the new session
        :return p: the packages for the user"""
        user_vector = self.user_obj.get_user_vector(self.k2k_obj)

        venues = self.nite_obj.get_nearby_venues(self.eavvs_obj, self.user_obj.get_order_preference[0],
                                                 self.user_obj.get_price_point)
        print(repr(venues))

        # venue_similarity = self.nite_obj.get_similarity(venues, user_vector)
        #
        # EAVVS object will have to be passed onto create packages so it can use get nearby venues
        # p = self.nite_obj.create_packages(self.k2k_obj, user_vector, venue_similarity,
        #                                   self.start_venue)
        # return p


# TODO: add new distance happiness to K2K similarity to get_similarity
# TODO: implement access to venue vectors from EAVVS crawler (may be separately networked)
# TODO: Alter create packages to use new venue object
packages = new_session(cli())