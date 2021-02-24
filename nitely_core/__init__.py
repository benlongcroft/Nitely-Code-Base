from nitely_core import Account, Preferences, User
import datetime

def str_to_coordinates(str_coordinates):
    """
    Converts comma separated coordinates to dictionary object of coordinates
    :param str_coordinates: comma separated (no spaces) coordinates in str type
    :return: dictionary {lat:[latitude], 'lng':[longitude]}
    """
    return {'lat': str_coordinates.split(",")[0], 'lng': str_coordinates.split(",")[1]}

def convert_to_datetime(start_time, end_time, date)
    try:
        _format_str = '%d%m%Y%H:%M'
        # should be in format DDMMYYYY
        _date_str = date
        start = datetime.datetime.strptime(_date_str + kwargs['start_time'],
                                                  _format_str)
        end = datetime.datetime.strptime(_date_str + kwargs['end_time'], _format_str)
        return start, end
        # converts date and time into datetime object

    except Exception as e:
        print('Error when transferring into datetime object')
        print(e)


class start_NITE:
    def __init__(self, kwargs):
        date = kwargs['date']
        location = str_to_coordinates(kwargs['location'])
        if kwargs['location_distance'] > 50:
            print("Distance is too far to accurately represent club_data")
        else:
            location_distance = kwargs['location_distance']
        keywords = kwargs['keywords']
        users_magic_words = kwargs['magic_words']
        start_time, end_time = convert_to_datetime(kwargs['start_time'],
                                                   kwargs['end_time'],
                                                   kwargs['date'])
        telephone = kwargs['telephone']
        user_name = kwargs['name']

        self.__user_account = Account(user_name, telephone)
        self.__user_preferences = Preferences(keywords,
                                              location,
                                              location_distance,
                                              users_magic_words,
                                              start_time,
                                              end_time)
        self.__user = User(Account, Preferences)

    def get_account(self):
        return self.__user_account

    def get_preferences(self):
        return self.__user_preferences

    def get_user(self):
        return self.__user

