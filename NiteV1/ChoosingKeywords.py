from tfidf import WordMetaData
import sqlite3
from matplotlib import pyplot as plt
import numpy as np
import TreeCreation as TC

TastingNotesDB = sqlite3.connect('TastingNotesDB.db') #open Tasting Notes DB
cursor = TastingNotesDB.cursor()
data = []
cursor.execute('''SELECT profile_text FROM Profiles''') # get all the data out of database and put it into list
DBresult = cursor.fetchall()
for x in DBresult:
    data.append(x[0].split(' '))

data = data[:100]
Meta = WordMetaData(data, len(data)) #create tfidf scores for every word in the data
print('Beginning to get TFIDF scores')
TfidfScores, SentimentScores = Meta.tfidfscore() #get TFIDF scores and Sentiment Scores

q=[]
mean = 0 
for key in TfidfScores.keys(): 
    value = TfidfScores[key]
    mean = mean+value[0] #calculate Ex of TFIDF Scores
    q.append([key, value[0]]) #transform in 2d List

mean = mean/len(q) #get Mean
q = TC.Sort2DList(q) #Sort TFIDF Scores 
stddev = np.std(np.array([x[1] for x in q])) #establish Standard deviation of scores

ub = mean + stddev #make upper boundry 1 stdev from mean
lb = min([x[1] for x in q])  #make lower boundry the minimum value (usually about 4)
p = []
for x in q:
    if x[1] >= ub: 
        continue
    elif x[1] <= lb:
        continue
    else:
        if SentimentScores[x[0]] != 0: #only add scores which have 'a' sentiment of some form and are between the boundrys
            p.append(x) 

# plt.plot([x[1]-2 for x in p], label = 'Trimmed')
# plt.plot([x[1] for x in q], label = 'Full')
# plt.show()
print(p)
print([x[0] for x in p[:10]]) #get 10 of the words that established above
print([1 for y in range(10)])
z = TC.RecursiveTreeCreation({}, [x[0] for x in p[:10]], [1 for y in range(10)], 0, 1, []) #make profile tree from those words
print(z)


