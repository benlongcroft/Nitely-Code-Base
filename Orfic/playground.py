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
#     db_obj = sqlite3.connect('/Users/benlongcroft/Documents/Orfic/Orfic/ClubDataDB.db')  # connect to database
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
#     db_obj = sqlite3.connect('/Users/benlongcroft/Documents/Orfic/Orfic/ClubDataDB.db')  # connect to database
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