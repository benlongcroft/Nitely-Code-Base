import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import random
import TreeCreation as TC
import Word2Vec as w2v
from sklearn.metrics.pairwise import cosine_similarity
from bokeh.plotting import figure, output_file, show
from scipy.spatial import distance

# prepare some data
def LoadRelevantVectors(ids, cursor, db):
    vectors = []
    for x in ids:
        cursor.execute('''SELECT vector FROM venue_vectors WHERE venue_id = ?''', (x,))
        r = cursor.fetchall()
        print(x)
        r = np.array([float(y) for y in r[0][0].split()])
        vectors.append(r)
    return vectors

def VectorisePreferences(keywords):
    scores = [1 for x in range(len(keywords))]
    return TC.turn_to_vector(TC.RecursiveTreeCreation({}, keywords, scores, 0, 1, []))

def GetClosestVector(ProfileVectors, vector):
    E = vector.reshape(1,300)
    highest = 0
    location = 0
    for z in range(len(ProfileVectors)):
        cos = distance.euclidian(E, ProfileVectors[z].reshape(1,300)) #must reshape numpy array to numpy matrix
        #^ this gets the cosine similarity between two vectors, maybe consider other metrics
        if cos > highest:
            highest = cos[0][0]
            location = z
    return highest, location #have to add one as the database ID's start at 1, not 0

NiteDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/ClubDataDB.db')
NiteCursor = NiteDB.cursor()
vectors = LoadRelevantVectors([x for x in range(1, 311)], NiteCursor, NiteDB)
q = open("/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubs.txt")
names = []
for r in q.readlines():
    r = r.strip()
    names.append(r)
d = dict(zip(names, vectors))
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
# for x in names:
#     d[x] = vectors[names.index(x)]
# df = pd.DataFrame(d)


# Attributes = [None]*8
# for a in range(8):
#     for v in vectors:
#         v = list(v)
#         if Attributes[a] != None:
#             Attributes[a].append(float(v[a]))
#         else:
#             Attributes[a] = [v[a]]
# print(len(Attributes))
df = pd.DataFrame(vectors)
# print(df)

# df.hist()   
# plt.bar()
q = [random.randint(0, len(vectors)) for x in range(3)]
samplev = []
samplen = []
for r in q:
    samplev.append(normalize(vectors[r]))
    samplen.append(names[r])

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness
r = lambda: random.randint(0,255)
g=0
word = 'latin'
d = normalize(w2v.GetWordVector(word))
for t in samplev:
    col = ('#%02X%02X%02X' % (r(),r(),r()))
    p.line([f for f in range(len(t))], t, line_width=2, color=col, legend_label=samplen[g])
    g=g+1
p.line([f for f in range(len(d))], d, line_width=2, color = "red", legend_label=word)
# show the results
show(p)
# for x in samplev:
#     plt.plot(x)
# # d = VectorisePreferences(['lively', 'chic', 'electric', 'new', 'luxurious', 'expensive'])
d = normalize(w2v.GetWordVector('latin'))
# plt.plot(d)
highest, location = GetClosestVector(samplev, d)
print(samplen[location])
print(highest)
# samplen.append('PERSONAL')
# plt.legend(samplen)
# plt.show()


