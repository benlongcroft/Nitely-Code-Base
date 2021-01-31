import pytest
from main import start_NITE
from nitely.user_preferences import create_packages, get_venues
from K2K.main import K2K
import random
import datetime
import math
from time import perf_counter
import pandas as pd
import numpy as np
from main import main


def get_random_keywords():
    all_words = open('all_words.txt', 'r')
    words = []
    for word in all_words.readlines():
        word = word.strip()
        words.append(word)

    number_of_words = random.randint(4, 10)
    keywords = []
    for i in range(number_of_words):
        keywords.append(random.choice(words))
    return keywords


def get_random_start_point(lat, lng):
    lat = (lat * math.pi / 180)
    lon = (lng * math.pi / 180)
    max_distance = 2000
    min_distance = 1
    earth_radius = 6_371_000
    distance = math.sqrt(
        random.random() * (max_distance ** 2 - min_distance ** 2) + min_distance ** 2)

    delta_lat = math.cos(random.random() * math.pi) * distance / earth_radius
    sign = random.randint(0, 2) * 2 - 1
    delta_lon = sign * math.acos(
        ((math.cos(distance / earth_radius) - math.cos(delta_lat)) /
         (math.cos(lat) * math.cos(delta_lat + lat))) + 1)

    return str((lat + delta_lat) * 180 / math.pi) + ',' + str((lon + delta_lon) * 180 / math.pi
                                                              )


def create_random_kwargs():
    return {
        'paid': random.choice([True, False]),
        'eighteen': random.choice([True, False]),
        'keywords': get_random_keywords(),
        'location': get_random_start_point(51.5085300, -0.1257400),
        'gay': False,
        'date': '06082001',
        'start_time': '19:00',
        'end_time': '03:00',
        'location_distance': random.randint(3, 49),
        'smartness': random.randint(1, 5),

    }
# change = True
# while True:
#     if change == True:
#         new_session = create_random_kwargs()
#     print(new_session)
#     user_obj = get_venues(new_session)
#     my_packages = create_packages(new_session)
#     k2k_obj = K2K(new_session['keywords'], [1 for x in range(len(new_session['keywords']))])
#     packages = main(start_NITE(user_obj, my_packages, k2k_obj, radius=4))
#     op = input('Change? (y/n): ')
#     if op.lower() == 'n':
#         change = False
#     else:
#         change = True
# user_obj.timings(selected_package)
