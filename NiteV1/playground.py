import sqlite3
import pickle
import numpy as np
# def punctremove(line):
#     punct = ''',./;'\[](){}:":<>?'''
#     nopunct = ""
#     for x in line:
#         if x not in punct:
#             nopunct = nopunct + x
#     return nopunct

# # f = open('/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubsMusicType.txt', "r")
# # r = f.readlines()
# # musictypes= []
# # for line in r:
# #     line = line.strip()
# #     line = line.split(',')
# #     for x in line:
# #         x = x.strip()
# #         if x == 'no music':
# #                 x = 'none'
# #         if x not in musictypes:
# #             musictypes.append(x)
# # print(musictypes)
# # f.close()

# # NiteDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/ClubDataDB.db')
# # cursor = NiteDB.cursor()
# # cursor.execute('''CREATE TABLE music_genres([genre_id] INTEGER PRIMARY KEY, [genre] VARCHAR(30))''')
# # NiteDB.commit()
# # for m in musictypes:
# #     cursor.execute('''INSERT INTO music_genres (genre) VALUES (?)''', (m,))
# # NiteDB.commit()
# # f = open('/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubsMusicType.txt', "w")
# # f.truncate()
# # for x in new:
# #     f.write(x+'\n')
# # f.close()
# f = open('/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubsVenueType.txt')
# r = f.readlines()
# vid = []
# for line in r:
#     line = line.lower()
#     line = line.split(',')
#     new = []
#     for x in line:
#         x = x.strip()
#         new.append(x)
#     vid.append(new)
# print(vid)

# cats = ['nightclub', 'sports bar', 'dj bar', 'cocktail bar', 'bar', 'bar & club', 'shisha bar', 'karaoke bar', 'restaurant', 'event space', 'super club', 'other', 'venue']
NiteDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/ClubDataDB.db')
cursor = NiteDB.cursor()
# # cursor.execute('''CREATE TABLE venue_to_type([venue_id] INTEGER, 
# #                                             [venue_type_id] INTEGER,
# #                                             FOREIGN KEY(venue_id) REFERENCES venues(venue_id), 
# #                                             FOREIGN KEY(venue_type_id) REFERENCES venue_types(venue_type_id))''')
# # NiteDB.commit()
# # command = '''INSERT INTO venue_to_type (venue_id, venue_type_id) VALUES (?, ?)'''
# # for i in range(len(vid)):
# #     venue_id = i+1
# #     for g in vid[i]:
# #         cursor.execute(command, (venue_id, (cats.index(g)+1),))
# # NiteDB.commit()
# f = open('/Users/benlongcroft/Documents/Nite/ClubData/Addresses.txt')
# r = f.readlines()
# r = [x.strip() for x in r]
# command = '''UPDATE venues SET address = ? WHERE venue_id = ?;'''
# t = 1
# for i in r:
#     cursor.execute(command, (i, t,))
#     t+=1
# NiteDB.commit()

# for x in range(312, 622):
#     cursor.execute('''DELETE FROM venues WHERE venue_id = ?''', (x,))
# NiteDB.commit()
# def normalize(v):
#     norm = np.linalg.norm(v)
#     if norm == 0: 
#        return v
#     return v / norm
# infile = open('/Users/benlongcroft/Documents/Nite/PickledVectors.vec','rb') #open binary file that has been pickled
# new_dict = pickle.load(infile) #load dictionary
# infile.close()
# ProfileVectors = list(new_dict.values())
# des = list(new_dict.keys())
# ProfileVectors.insert(238, ProfileVectors[237])
# des.insert(238, des[237])

# venue_id = 1
# command = ('''INSERT INTO venue_vectors (venue_id, vector) VALUES (?, ?)''')
# for v in ProfileVectors:
#     v = normalize(v)
#     v = [str(x) for x in v]
#     v = ' '.join(v) #change this to compression at a later date, but convenient for now!
#     cursor.execute(command, (venue_id, v,))
#     venue_id += 1
# NiteDB.commit()