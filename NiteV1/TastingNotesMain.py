from PrepareData import CreateDatabase
import TreeCreation as TC
from tfidf import WordMetaData
import Word2Vec
import sqlite3
import Word2Vec as w2v
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import time


def GetVector(doc, TfidfScores, SentimentScores):
    words = []
    scores = []
    temp = TC.GetKeywords(doc, TfidfScores, SentimentScores)
    for x in temp:
        words.append(x[0])
        scores.append(x[1])
    z = TC.turn_to_vector(TC.RecursiveTreeCreation({}, words, scores, 0, 1, []))
    return z

def VectorisePreferences(keywords):
    scores = [1 for x in range(len(keywords))]
    return TC.turn_to_vector(TC.RecursiveTreeCreation({}, keywords, scores, 0, 1, []))

def GetVectors(data, splitpoint = None):
    if splitpoint != None:
        data = data[:splitpoint]
    ProfileVectors = []
    for doc in data:
        z = GetVector(doc, TfidfScores, SentimentScores)
        #Make profile tree, rescore it and then turn it into a vector
        ProfileVectors.append(z)
    return ProfileVectors

def OutputProfile(filepath, linenumber):
    fp = open(filepath)
    for q, line in enumerate(fp):
        if q == linenumber:
            print(line) #prints the full description of the club before keyword analysis
        elif q > linenumber:
            break
    fp.close()

def GetClosestVector(ProfileVectors, vector, filepath):
    # OutputProfile(filepath, pointer)
    E = vector.reshape(1,300)
    highest = 0
    location = 0
    for z in range(len(ProfileVectors)):
        cos = cosine_similarity(E, ProfileVectors[z].reshape(1,300)) #must reshape numpy array to numpy matrix
        #^ this gets the cosine similarity between two vectors, maybe consider other metrics
        print(cos)
        if cos > highest:
            highest = cos[0][0]
            location = z
    return highest, location

def SaveVectors(filepath, ProfileVectors, data, splitpoint):
    dictToPickle = {}
    if splitpoint != None: #if not all the data has been turned to a profile vectors (due to performancea and/or time requirements)
        data = data[:splitpoint] #only get data up to certain index
    for index in range(len(data)):
        dictToPickle[' '.join(data[index])] = ProfileVectors[index] #turn data into a dictionary where the key is the profile description pre-keywording (after lemmatising)
    outfile = open(filepath,'wb') #create a binary file with name as filepath 
    pickle.dump(dictToPickle,outfile) #dump dictionary
    outfile.close()

def OpenSavedVectors(filepath):
    infile = open(filepath,'rb') #open binary file that has been pickled
    new_dict = pickle.load(infile) #load dictionary
    infile.close()
    data = list(new_dict.keys())
    for x in range(len(data)):
        data[x] = data[x].split(' ')
    ProfileVectors = list(new_dict.values())
    return data, ProfileVectors

open("./TastingNotesDB.db", "w")
cursor, TastingNotesDB = CreateDatabase("./ClubDes.txt") #load data out of csv into database

print('Created Database')
TastingNotesDB = sqlite3.connect('TastingNotesDB.db')
cursor = TastingNotesDB.cursor()
data = []
print('Inserting data into python object')
cursor.execute('''SELECT profile_text FROM Profiles''') # get all the data out of database and put it into list
DBresult = cursor.fetchall()
for x in DBresult:
    data.append(x[0].split(' '))

print('Data loaded')
Meta = WordMetaData(data, len(data)) #create tfidf scores for every word in the data
print('Beginning to get TFIDF scores')
TfidfScores, SentimentScores = Meta.tfidfscore()
print('TFIDF scores logged')

print('Calculating vectors')

# ProfileVectors = get_vectors(data, None)
data, ProfileVectors = OpenSavedVectors("PickledVectors.vec")
print('Profile vectors created')
print('Saving vectors to pickle file')
# SaveVectors("PickledVectors.vec", ProfileVectors, data, None)
VectorToTry = ['chic', 'electric', 'exciting', 'new', 'luxurious', 'cool']

# highest, location = GetClosestVector(ProfileVectors, 5, './ClubDes.txt')
z = VectorisePreferences(VectorToTry)
highest, location = GetClosestVector(ProfileVectors, z, './ClubDes.txt')
print('Getting Closest Vector to 90')
print('Job complete:\n')
print("Highest Score: ", highest)
print('Location: ', location)
print('\n')
OutputProfile("./ClubDes.txt", location)
# OutputProfile("./ClubDes.txt", 5)
print(TC.GetKeywords(data[location], TfidfScores, SentimentScores))
# print(TC.GetKeywords(data[5], TfidfScores, SentimentScores))

