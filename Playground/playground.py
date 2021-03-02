# import sqlite3
# from keras.models import Sequential, save_model, load_model
# from keras.layers import Dense
# from keras.models import model_from_json
# import numpy as np
# import random
#
# def make_pretty(db_output):
#     newlist = []
#     for vector in db_output:
#         vector_str = vector[0]
#         vector = np.array([float(x) for x in vector_str.split(' ')]).reshape(1, 300)
#         newlist.append(vector)
#     return np.array(newlist)
#
# def get_data():
#     db_obj = sqlite3.connect('/Users/benlongcroft/Documents/Nitely/Nitely/ClubDataDB.db')  # connect to database
#     cursor_obj = db_obj.cursor()  # instantiate a cursor for db
#
#     _command = '''SELECT venue_vectors.vector FROM venue_vectors, venue_to_type
#     WHERE venue_vectors.venue_id = venue_to_type.venue_id AND venue_to_type.venue_type_id = 1 OR venue_to_type.venue_type_id = 11'''
#     cursor_obj.execute(_command)
#     AllIntenseVenuesX = cursor_obj.fetchall()
#
#     _command = '''SELECT venue_vectors.vector FROM venue_vectors, venue_to_type
#     WHERE venue_vectors.venue_id = venue_to_type.venue_id AND venue_to_type.venue_type_id = 4
#     OR venue_to_type.venue_type_id = 5 OR venue_to_type.venue_type_id = 2'''
#     cursor_obj.execute(_command)
#     AllMildVenuesX = cursor_obj.fetchall()
#
#     AllData = AllIntenseVenuesX + AllMildVenuesX
#     AllScores = [1 for x in range(len(AllIntenseVenuesX))] + [0 for y in range(len(AllMildVenuesX))]
#
#     AllData = make_pretty(AllData)
#
#     LengthOfAllData = len(AllData)
#     TrainLength = int(round(0.8 * LengthOfAllData))
#
#     TrainX = np.array(AllData[:TrainLength]).reshape(TrainLength, 300)
#     print(TrainX.shape)
#     TrainY = np.array(AllScores[:TrainLength]).reshape(TrainLength, 1)
#     print(TrainY.shape)
#     TestX = np.array(AllData[TrainLength:]).reshape(LengthOfAllData-TrainLength, 300)
#     print(TestX.shape)
#     TestY = np.array(AllScores[TrainLength:]).reshape(LengthOfAllData-TrainLength, 1)
#     print(TestY.shape)
#
#     return TrainX, TrainY, TestX, TestY
#
# def save_keras_model(model):#save model to json file
#     model_json = model.to_json() #abracadabra
#     with open("intensity_weights.json", "w") as json_file: #open json file
#         json_file.write(model_json) #write our jsoned model
#     # serialize weights to HDF5
#     model.save_weights("intensity_weights.h5") #save the weights in a HDF5 format
#     print("Saved model to disk in current directory") #print output message
#
# def open_saved_model(path_to_file, path_to_weights):
#     json_file = open(path_to_file, 'r') #open file in read only format
#     loaded_model_json = json_file.read() #read the model
#     json_file.close() #close the file
#     loaded_model = model_from_json(loaded_model_json) #change from json file to model
#     # load weights into new model
#     loaded_model.load_weights(path_to_weights) #open loaded weights
#     print("Loaded model from disk")
#     return loaded_model
# #
# # TrainX, TrainY, TestX, TestY = get_data()
# # print(len(TrainX), len(TrainY))
# # print(len(TestX), len(TestY))
# #
# # model = Sequential()
# # model.add(Dense(200, input_dim=300, activation='relu'))
# # model.add(Dense(250, activation='relu'))
# # model.add(Dense(50, activation='relu'))
# # model.add(Dense(1, activation='sigmoid'))
# #
# # model.compile(loss='mse', optimizer='adagrad', metrics=['accuracy'])
# # history = model.fit(TrainX, TrainY, epochs=150, batch_size=10, shuffle=True)
# # scores = model.evaluate(TestX, TestY)
# # print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
# # save_model(model, './saved_model')
#
# def Testing(venue_id, model):
#     db_obj = sqlite3.connect('/Users/benlongcroft/Documents/Nitely/Nitely/ClubDataDB.db')  # connect to database
#     cursor_obj = db_obj.cursor()  # instantiate a cursor for db
#     _command = '''SELECT venue_vectors.vector FROM venue_vectors WHERE venue_id = ?'''
#     cursor_obj.execute(_command, (venue_id, ))
#     params = cursor_obj.fetchall()
#     params = params[0][0]
#     vector = np.array([float(x) for x in params.split(' ')]).reshape(1, 300)
#     print(model.predict(vector))
#
# model = load_model('./saved_model')
# Testing(2, model)
# import requests
# import pandas as pd

# def CheckWordCount(input_list):
#     return len(input_list.split(' '))
# link = "https://www.skiddle.com/api/v1/venues/?&type=n" \
#        "&api_key=6cb3113b3e7ba52fb4c981580f2b0b46" \
#        "&latitude=51.4978793&longitude=-0.0039635&radius=10" \
#        "&limit=100&description=1"
# r = requests.get(link)
# r = r.json()
# df = pd.DataFrame(r['results'])
# pd.set_option('display.max_columns', None)
# print(df)
# # ids = list(df['id'])
# # descriptions = list(df['description'])
# #
# # for x in range(len(descriptions)):

import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import sqlite3
from random import shuffle
import time
#
# def googleSearch(query):
#     g_clean = [ ]
#     # url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
#     url = 'https://www.google.com/search?channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
#     try:
#         html = requests.get(url)
#         print(html)
#         if html.status_code==200:
#             soup = BeautifulSoup(html.text, 'lxml')
#             a = soup.find_all('a')
#             for i in a:
#                 k = i.get('href')
#                 try:
#                     m = re.search("(?P<url>https?://[^\s]+)", k)
#                     n = m.group(0)
#                     rul = n.split('&')[0]
#                     domain = urlparse(rul)
#                     if(re.search('google.com', domain.netloc)):
#                         continue
#                     else:
#                         g_clean.append(rul)
#                 except:
#                     continue
#     except Exception as ex:
#         print(ex)
#     finally:
#         return g_clean
#
# def CheckLink(url, name, town):
#     base = "https://www.designmynight.com/"
#     if base in url:
#         if '/'+name+'/' in url and '/'+town+'/':
#             return url
#
# db_obj = sqlite3.connect('//skiddle/venues_skiddle.db')
# cursor_obj = db_obj.cursor()
#
# cursor_obj.execute('SELECT name, town FROM venues')
# venues = cursor_obj.fetchall()
# shuffle(venues)
# for v in venues:
#     time.sleep(1)
#     searchterm = (v[0]+' '+v[1]+' '+'designmynight.com')
#     print(searchterm)
#     links = googleSearch(searchterm)
#     print(links)
#     for l in links:
#         u = CheckLink(l, v[0], v[1])
#         print(u)
#         html = requests.get(u)
#         if html.status_code == 200:
#             soup = BeautifulSoup(html.text, 'lxml')
#             try:
#                 l = soup.find("section", class_="row line-height-2x")
#                 description = l.text
#                 print(description)
#             except:
#                 print(u)
#                 print('Cant find description')
#
# html = requests.get(url)
# if html.status_code == 200:
#     soup = BeautifulSoup(html.text, 'lxml')
#     l = soup.find("section", class_="row line-height-2x")
#     print(l.text)

import sqlite3
import pickle

db_obj = sqlite3.connect(
    '/Users/benlongcroft/Documents/Nitely Project/Nitely/VENUES.db')
cursor_obj = db_obj.cursor()

pickle_off = open("/Users/benlongcroft/Documents/Nitely Project/Nitely/club_vectors_not_normalised.txt", "rb")
#using 0.75-1
vectors = pickle.load(pickle_off)
cursor_obj.execute('''SELECT id FROM venue_info  WHERE description != "DO NOT USE"''')
ids = [x[0] for x in cursor_obj.fetchall()]
print(len(ids))
print(len(vectors))
for i, _ in enumerate(ids):
    vector = str(vectors[i][0])
    vector = vector.replace('[', '')
    vector = vector.replace(']', '')
    vector = vector.replace('\n', '')
    cursor_obj.execute('''UPDATE venue_info SET vector = ? WHERE id = ?''', (str(vector), ids[i],))
db_obj.commit()

# cursor_obj.execute('''SELECT DISTINCT venue_id FROM by_week WHERE venue_id IN (SELECT id FROM venue_info  WHERE description = 'DO NOT USE') ORDER BY venue_id ASC''')
# venue_ids = [x[0] for x in cursor_obj.fetchall()]
not_use = [111, 152, 186, 212, 220]
# cursor_obj.execute('''SELECT id FROM venue_info  WHERE description != 'DO NOT USE' ORDER BY id ASC''')
# q = [x[0] for x in cursor_obj.fetchall()]
# print(venue_ids)
# print(q)
# no_words = ['glamour', 'famous', 'opulent', 'famous', 'family', 'old worldy', 'party']
# cursor_obj.execute('''SELECT id, description FROM venue_info''')
# data = [x for x in cursor_obj.fetchall() if x[0] not in not_use]
# descriptions = [x[1] for x in data]
# dictionary = {}
# for document in descriptions:
#     orig = document
#     document = document.split(', ')
#     for word in document:
#         word = word.lower()
#         if word in no_words:
#             print(data[descriptions.index(orig)])
#         if word in dictionary:
#             dictionary[word] = dictionary[word] + 1
#         else:
#             dictionary[word] = 1
#
# sorted_dict = {}
# sorted_keys = sorted(dictionary, key=dictionary.get)  # [1, 3, 2]
#
# for w in sorted_keys:
#     sorted_dict[w] = dictionary[w]
#
# print(sorted_dict)
# import pickle
# import random
#
# pickle_off = open("club_vectors_30-01-2021.txt", "rb")
# vectors = pickle.load(pickle_off)
# print(len(vectors))
# cursor_obj.execute('''SELECT id FROM venue_info  WHERE description != 'DO NOT USE';''')
# ids = [x[0] for x in cursor_obj.fetchall()]
#
# from scipy.spatial import distance
#
#
# def get_similarity(vectors, ids):
#     for i, vec1 in enumerate(vectors):
#         vec1_id = ids[i]
#         for x, vec2 in enumerate(vectors):
#             vec2_id = ids[x]
#             print('Similarity:', vec1_id, '-', vec2_id, '-->', distance.euclidean(vec1, vec2))
#
#
# random_vector_index = lambda: random.randint(0, len(vectors) - 1)
# q = [random_vector_index() for x in range(3)]
# vec_ids = [ids[x] for x in q]
# vectors = [vectors[x] for x in q]
# print(vec_ids)
# get_similarity(vectors, vec_ids)
#
#
# def find_similar(vectors, ids, vec):
#     scores = []
#     for i, vector in enumerate(vectors):
#         scores.append([ids[i], distance.euclidean(vector, vec)])
#     return sorted(scores, key=lambda l: l[1], reverse=True)

# find_similar(vectors, ids, vectors[171])