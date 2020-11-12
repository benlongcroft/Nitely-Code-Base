# import requests
# import sqlite3
#
# geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
# api_key = "AIzaSyAAQ2bYW5ZsFg3VUoms-BxkeO5NCafGu5o"
# #use google maps API
# db_obj = sqlite3.connect('./ClubDataDB.db') #connect to database
# cursor_obj = db_obj.cursor()
#
# command = '''SELECT address FROM venues WHERE venue_id=?''' #generate base command
# y=[]
# for x in range(1, 311):
#     cursor_obj.execute(command, (x,))
#     y_address = cursor_obj.fetchall()
#     y_address = y_address[0][0]
#     print(y_address)
#     response = requests.get(geo_url, params={'address':y_address, 'key':api_key})
#     #insert address into requests module
#     results = response.json()['results'][0]
#     y_coordinates = results['geometry']['location']
#     y_coordinates = str(y_coordinates['lat'])+','+str(y_coordinates['lng'])
#     print(y_coordinates)
#     y.append(y_coordinates)
#     print('\n')
#
# command = "UPDATE venues SET address=? WHERE venue_id=?"
# for x in range(len(y)):
#     venue_id = x+1
#     cursor_obj.execute(command, (y[x], venue_id,))
#     db_obj.commit()

# from bokeh.plotting import figure, output_file, show
# import spacy
#
# nlp = spacy.load('en_core_web_md', disable=['parser'])
# word = nlp.vocab['lively']
# d = []
# for x in word.vocab:
#     d.append(x.prob)
# output_file("lines.html")
# p = figure(title="Distribution of spaCy probs", x_axis_label='x', y_axis_label='y')
#
# p.BoxPlot(d)
# show(p)

# import en_core_web_lg
# import pickle
# nlp = en_core_web_lg.load()
#
# if nlp.vocab.lookups_extra.has_table("lexeme_prob"):
#     nlp.vocab.lookups_extra.remove_table("lexeme_prob")
#
# lexemes = []
# for orth in nlp.vocab.vectors:
#     if nlp.vocab[orth].prob >= -10:
#         lexemes.append(nlp.vocab[orth])
#
# with open('lexemes.pkl', 'wb') as f:
#     pickle.dump(lexemes, f)
#
# import en_core_web_lg
# from spacy.lang.en import English
# import spacy.util
#
# nlp = en_core_web_lg.load()
# print(len(nlp.vocab))
# if nlp.vocab.lookups_extra.has_table("lexeme_prob"):
#     nlp.vocab.lookups_extra.remove_table("lexeme_prob")
#
# new_vocab = English.Defaults.create_vocab()
# new_vocab.vectors = nlp.vocab.vectors
# new_vocab.lookups = nlp.vocab.lookups
#
# x = 0
# for lex in nlp.vocab:
#     if lex.prob >= -15:
#         new_vocab[lex.orth_] # this adds a lexeme
#         new_vocab[lex.orth_].prob = lex.prob
#         x=x+1
#
# nlp.vocab = new_vocab
#
#
# print(len(nlp.vocab))
# for name, pipe in nlp.pipeline:
#     if hasattr(pipe, "cfg") and pipe.cfg.get("pretrained_vectors"):
#         pipe.cfg["pretrained_vectors"] = nlp.vocab.vectors.name
# nlp.to_disk("reduced_model")
# nlp = spacy.load("reduced_model")
# import spacy
# import pickle
#
# nlp = spacy.load('en_core_web_md', disable=['parser', 'tagger', 'ner'])
#
# lexemes = []
# if nlp.vocab.lookups_extra.has_table("lexeme_prob"):
#     nlp.vocab.lookups_extra.remove_table("lexeme_prob")
# #
# for orth in nlp.vocab.vectors:
#     if nlp.vocab[orth].prob >= -12:
#         lexemes.append(nlp.vocab[orth])
#
# lexemes = [x.text for x in lexemes]
# with open('lexemes.pkl', 'wb') as f:
#     pickle.dump(lexemes, f)
#
# import requests
# import pandas as pd
# command = 'https://www.skiddle.com/api/v1/events/search/'
# Args = {'api_key':'6cb3113b3e7ba52fb4c981580f2b0b46', 'latitude':'51.488797',
#         'longitude':'-0.141731', 'radius':'4',
#         'eventcode':'CLUB', 'order':'distance',
#         'ticketsavailable':'1'}
# response = requests.get(command, params=Args)
# c = response.json()['results']
# pd.set_option('display.max_columns', None)
# print(c)
# results = pd.DataFrame(c)
# print(results)

# import sqlite3
# db_obj = sqlite3.connect('./ClubDataDB.db')  # connect to database
# cursor_obj = db_obj.cursor() # instantiate a cursor for db
#
# venue_type = open('./ClubData/AllLondonClubsVenueType.txt')
# d = {'nightclub':1, 'sports bar':2, 'dj bar':3, 'cocktail bar':4, 'bar':5,
# 'bar & club':6, 'shisha bar':7, 'karaoke bar':8, 'restaurant':9, 'event space':10,
# 'super club':11, 'other':12, 'venue':13}
#
# venues = []
# for x in venue_type.readlines():
#         x = x.lower()
#         x = x.strip('\n')
#         x = x.split(', ')
#         x = [y.strip() for y in x]
#         x = [d[y] for y in x]
#         venues.append(x)
#
# command = '''INSERT INTO venue_to_type (venue_id, venue_type_id) VALUES (?, ?)'''
# z = 0
# for x in range(len(venues)):
#         venue_id = x+1
#         for y in venues[x]:
#                 cursor_obj.execute(command, (venue_id, y,))
#                 z=z+1
#         db_obj.commit()
# print(z)
