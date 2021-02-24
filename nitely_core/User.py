from Account import account
from Preferences import preferences


class user(preferences, account):
    def __init__(self, user_preferences, user_account):
        self.__keywords = user_preferences.get_keywords
        self.__location = user_preferences.get_location
        self.__location_distance = user_preferences.get_location_distance
        self.__magic_words = user_preferences.get_magic_words
        self.__start_time = user_preferences.get_start_time
        self.__end_time = user_preferences.get_end_time
        preferences.__init__(self, self.__keywords, self.__location, self.__location_distance,
                             self.__magic_words, self.__start_time, self.__end_time)
        self.__name = user_account.get_name
        self.__telephone = user_account.get_telephone
        account.__init__(self, self.__name, self.__telephone)

    def get_user_vector(self, K2K):
        return K2K.get_user_vector
