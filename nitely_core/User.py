from Account import account
from Preferences import preferences

class user(account, preferences):
    def __init__(self, user_account, user_preferences):
        self.__name = user_account.get_name()
        self.__telephone = user_account.get_telephone()

        self.__keywords = user_preferences.get_keywords()
        self.__location = user_preferences.get_location()
        self.__location_distance = user_preferences.get_location_distance()
        self.__magic_words = user_preferences.get_magic_words()
        self.__start_time = user_preferences.get_start_time()
        self.__end_time = user_preferences.get_end_time()

    def get_user_vector(self, K2K):
        return K2K.get_user_vector()
