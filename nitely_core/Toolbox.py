from geopy.distance import geodesic
import datetime
import random


def find_max_in_dict(dictionary):
    max_key = ''
    max_value = 0
    for key in dictionary.keys():
        value = dictionary[key]
        if value > max_value:
            max_key = key
    return max_key


def sort_dictionary(dict1):
    sorted_dict = {}
    sorted_keys = sorted(dict1, key=dict1.get, reverse=True)
    for w in sorted_keys:
        sorted_dict[w] = dict1[w]
    return sorted_dict


def get_head_of_dict(dictionary, length):
    head = {}
    for x in range(length):
        key = list(dictionary.keys())[x]
        head[key] = dictionary[key]
    return head


def str_to_coordinates(str_coordinates):
    """
    Converts comma separated coordinates to dictionary object of coordinates
    :param str_coordinates: comma separated (no spaces) coordinates in str type
    :return: dictionary {lat:[latitude], 'lng':[longitude]}
    """
    return {'lat': str_coordinates.split(" ")[0], 'lng': str_coordinates.split(" ")[1]}


def convert_to_datetime(start_time, end_time, date):
    """
    Converts string start_time, end_time and date into datetime objects
    :param start_time: String start time
    :param end_time: String end time
    :param date: String date in format DDMMYYYY
    :return: start_time and end_time with dates in datetime format
    """
    try:
        _format_str = '%d%m%Y%H:%M'
        # should be in format DDMMYYYY
        _date_str = date
        start = datetime.datetime.strptime(_date_str + start_time,
                                           _format_str)
        end = datetime.datetime.strptime(_date_str + end_time, _format_str)
        if start.time() > end.time():
            end = end + datetime.timedelta(days=1)
        return start, end
        # converts date and time into datetime object

    except Exception as e:
        print('Error when transferring into datetime object')
        print('Probably invalid format for conversion')
        print(e)


def date_str_to_weekday(date):
    format_str = "%d%m%Y"
    d = datetime.datetime.strptime(date, format_str)
    return d.strftime("%a").upper()


def get_distance_between_coords(current_location, y_coordinates):
    """
    Gets distance as crow flies between two addresses

    :param current_location: Users current location in coordinates
    :param y_coordinates: location to travel to in coordinates
    :return: Distance in miles between coordinates
    """
    # use geopy geodesic module to get distance in miles and return it to function call
    return geodesic((y_coordinates['lat'], y_coordinates['lng']),
                    (current_location['lat'], current_location['lng'])).miles


def delete_duplicates(new_venues, used_venues):
    return_list = []
    ids = [x.get_id for x in used_venues]
    for venue in new_venues:
        if venue.get_id not in ids:
            return_list.append(venue)

    return return_list


def db_to_type(type, restaurant, club):
    type_to_bin = {'pub': '000', 'bar': '001', 'club': '010', 'other': '011', 'live': '100'}
    return type_to_bin[type.lower()] + str(restaurant) + str(club)
