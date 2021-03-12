import sqlite3
from vector_k2k import K2K
from math import log
from statistics import stdev
from time import perf_counter


def weight(word, m, n):
    magic_words = {'food', 'theme', 'dj', 'beer', 'brunch', 'traditional',
                   'cocktails', 'terrace', 'live', 'wine', 'sports', 'gay',
                   'bar', 'pub', 'club', 'other'}
    if word in magic_words:
        return m
    else:
        return n


def create(descriptions, magic, normal):
    done = 0
    club_vectors_total = []
    time_taken = []
    for d in descriptions:
        if d[0] == 'DO NOT USE':
            continue
        else:
            t1_start = perf_counter()
            f = open(
                "/Users/benlongcroft/Documents/Nitely Project/Nitely/vector_k2k/transpositiontbl.pkl",
                "w")
            f.truncate()
            f.close()
            k = K2K(d, [weight(x, magic, normal) for x in d])
            print(d)
            print([weight(x, magic, normal) for x in d])
            club_vectors_total.append(k.get_user_vector)

            done = done + 1
            t2_end = perf_counter()
            time_taken.append(t2_end - t1_start)
            seconds_total = (sum(time_taken) / len(time_taken)) * (len(descriptions) - done)
            print('Total time remaining in seconds:', seconds_total)
    return club_vectors_total


db = sqlite3.connect('/Users/benlongcroft/Documents/Nitely Project/Nitely/VENUES.db')
cur = db.cursor()
import pickle

cur.execute('''SELECT description, type FROM venue_info WHERE description != "DO NOT USE"''')
descriptions = []
for item in cur.fetchall():
    des = item[0].split(', ')
    des.append(item[1])
    words = []
    for x in list(set(des)):
        if x != '':
            words.append(x)

    descriptions.append(words)

# values = [(1, 0.9), (1, 0.8), (1, 0.7), (1, 0.6), (1, 0.5)]
# for x, y in values:

f = open("/Users/benlongcroft/Documents/Nitely Project/Nitely/vector_k2k/transpositiontbl.pkl", "w")
f.truncate()
f.close()
cvt = create(descriptions, 1, 1)
with open('club_vectors_normalised_1.txt', 'wb') as fh:
    pickle.dump(cvt, fh)

# TODO: Create a 'some of our favourites section' which are handpicked routes through newcastle
#  - delegate to Hugo?
