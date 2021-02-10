import sqlite3
from vector_k2k import K2K
from math import log
from statistics import stdev
from time import perf_counter


def weight(word):
    magic_words = {'food', 'theme', 'dj', 'beer', 'brunch', 'traditional',
                   'cocktails', 'terrace', 'live', 'wine', 'sports', 'gay',
                   'bar', 'pub', 'club', 'other'}
    if word in magic_words:
        return 0.5
    else:
        return 1


db = sqlite3.connect('/Users/benlongcroft/Documents/Nitely Project/NewDB/ExperimentalOrficDB.db')
cur = db.cursor()

cur.execute('''SELECT description, type FROM venue_info WHERE description != "DO NOT USE"''')
descriptions = []
for item in cur.fetchall():
    des = item[0].split(', ')
    des.append(item[1])
    descriptions.append(list(set(des)))

done = 0
club_vectors_total = []
time_taken = []
for d in descriptions:
    if d[0] == 'DO NOT USE':
        continue
    else:
        t1_start = perf_counter()
        k = K2K(d, [weight(x) for x in d])
        print(d)
        print([weight(x) for x in d])
        club_vectors_total.append(k.get_user_vector)

        done = done + 1
        t2_end = perf_counter()
        time_taken.append(t2_end - t1_start)
        seconds_total = (sum(time_taken) / len(time_taken)) * (len(descriptions) - done)
        print('Total time remaining in seconds:', seconds_total)

# TODO: Create a 'some of our favourites section' which are handpicked routes through newcastle
#  - delegate to Hugo?
