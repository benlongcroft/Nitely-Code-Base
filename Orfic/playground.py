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
