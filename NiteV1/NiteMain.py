from PrepareData import CreateDatabase
import TreeCreation as TC
from tfidf import WordMetaData
import Word2Vec
import sqlite3
import Word2Vec as w2v
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from scipy.spatial import distance
import pickle
from bokeh.plotting import figure, output_file, show
import random


def GetVector(doc, TfidfScores, SentimentScores): #enter doc as string
    words = []
    scores = []
    print(doc)
    temp = TC.GetKeywords(doc, TfidfScores, SentimentScores)
    print(temp)
    for x in temp:
        words.append(x[0])
        scores.append(x[1])
    z = TC.TurnToVector(TC.RecursiveTreeCreation({}, words, scores, 0, 1, []))
    return z

def VectorisePreferences(keywords):
    scores = [1 for x in range(len(keywords))]
    return TC.TurnToVector(TC.RecursiveTreeCreation({}, keywords, scores, 0, 1, []))

def GetVectors(data, splitpoint, TfidfScores, SentimentScores):
    if splitpoint != None:
        data = data[:splitpoint]
    ProfileVectors = []
    for doc in data:
        print(data.index(doc))
        z = GetVector(doc, TfidfScores, SentimentScores)
        #Make profile tree, rescore it and then turn it into a vector
        ProfileVectors.append(z)
    return ProfileVectors

def PrintVenueRecord(VenueID, cursor, db):
    cursor.execute('''SELECT * FROM venues WHERE venue_id = ?''', (VenueID,))
    r = cursor.fetchall()[0]
    record = []
    for e in r[0:]:
        record.append(e)
    print('Name:',record[1], 'Door Charge:', record[5], 'Dress Code:', record[6])
    print('Description:', record[2])
    print('Address:', record[-1])
    print('\n')

def GetClosestVector(ProfileVectors, vector):
    E = vector.reshape(1,300)
    location = 0
    scores = []
    for z in range(len(ProfileVectors)):
        cos = distance.euclidean(E, ProfileVectors[z].reshape(1,300)) #must reshape numpy array to numpy matrix
        #^ this gets the euclidian distance between two vectors, maybe consider other metrics
        scores.append([cos,z])
    scores = sorted(scores, key=lambda x:x[0], reverse=False)
    return scores[:5]

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

def LoadRelevantVectors(ids, cursor, db):
    vectors = []
    for x in ids:
        cursor.execute('''SELECT vector FROM venue_vectors WHERE venue_id = ?''', (x,))
        r = cursor.fetchall()
        r = np.array([float(y) for y in r[0][0].split()])
        vectors.append(preprocessing.normalize(r.reshape(1,300)))
    return vectors
    

def RefineData(db, cursor):
    print('''Age Restriction:\n1) Over 18's\n2) Over 21's\n3) None''')
    AgeRestriction = int(input("Age Restriction: "))
    if AgeRestriction == 1:
        AgeRestriction = 'over 18s'
    elif AgeRestriction == 2:
        AgeRestriction = 'over 21s'
    else:
        AgeRestriction = 'none'
    print('''Dress Code (number between 1-5, 0 to leave blank)''')
    DressCode = int(input("Dress Code: "))
    print('''Entry Price:\n1) Free\n2) I don't mind paying''')
    EntryPrice = int(input("Entry Price: "))
    if EntryPrice == 1:
        EntryPrice = 'no door charge'
    print('''1|nightclub\n
             2|sports bar\n
             3|dj bar\n
             4|cocktail bar\n
             5|bar\n
             6|bar & club\n
             7|shisha bar\n
             8|karaoke bar\n
             9|restaurant\n
            10|event space\n
            11|super club\n
            12|other\n
            13|venue\n''')
    print('type DONE when entered all venue types')
    venue_types = []
    while True:
        c = input("Venue Type: ")
        if c == 'DONE':
            break
        else:
            venue_types.append(int(c))
    command = ('''SELECT venue_id FROM venues WHERE age_restriction = ?''')
    args = [AgeRestriction]
    if DressCode != 0:
        command = (command +''' AND dress_rating <= ?''')
        args.append(DressCode)
    if EntryPrice == 'no door charge':
        command = (command + ''' AND entry_price = ?''')
        args.append(EntryPrice)
    cursor.execute(command, tuple(args,))
    d = cursor.fetchall()
    preliminary_venues = [y[0] for y in d]
    command = ('''SELECT venue_id FROM venue_to_type WHERE venue_to_type.venue_type_id = ?''')
    # applicable_venues = []
    # for venue_id in preliminary_venues:
    #     cursor.execute(command, (venue_id,))
    #     types = [x[0] for x in cursor.fetchall()]
    #     for t in types:
    #         if int(t) in venue_types:
    #             applicable_venues.append(venue_id)
    #             break
    venues_of_type = []
    for venue_id in venue_types:
        cursor.execute(command, (venue_id,))
        q = cursor.fetchall()
        venues_of_type.extend([y[0] for y in q])
    applicable_venues = []
    for vid in preliminary_venues:
        if int(vid) in venues_of_type:
            applicable_venues.append(vid)
    if len(applicable_venues) < 15:
        print('Getting similar results as criteria too specific')
        d = random.choices(venues_of_type, k=12)
        applicable_venues.extend(d)
    
    return applicable_venues

    return applicable_venues
def login(db, cursor):
    print('Logging in!')
    mobile = input('Enter your mobile number: ')
    print(mobile)
    cursor.execute('''SELECT user_id FROM users WHERE mobile = ?''', (mobile,))
    if len(cursor.fetchall()) != 0:
        return (cursor.fetchall())
    else:
        return -1

def rate_previous_experience():
    print('Please take some time to rate your previous experience!')
    r = input('Enter a score (1-5) where 5 is the best: ')
    return r

def add_rating_to_database(user_id, rating, db, cursor):
    cursor.execute('''UPDATE last_experience SET rating = ? WHERE user_id = ?''', (rating, user_id,))
    db.commit()

def register(db, cursor):
    fn = input('Enter First Name: ')
    ln = input('Enter Last Name: ')
    e = input('Enter email: ')
    m = input('Enter mobile number: ')
    cursor.execute('''INSERT INTO users(first_name, last_name, email, mobile) VALUES (?, ?, ?, ?)''', (fn.lower(), ln.lower(), e.lower(), m,))
    db.commit()
    return login(db, cursor)

def add_experience(user_id, db, cursor, vector):
    cursor.execute('''INSERT INTO last_experience(user_id, vector) VALUES (?, ?)''', (user_id, vector,))
    db.commit()
# open("/Users/benlongcroft/Documents/Nite/ClubDataDB.db", "w")
# cursor, NiteDB = CreateDatabase("/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubs") #load data out of csv into database
NiteDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/ClubDataDB.db')
NiteCursor = NiteDB.cursor()
UserDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/RegistrationDB.db')
UserCursor = UserDB.cursor()


# op = input('Are you already registered? (y/n): ')
# if op.lower() == 'y':
#     user_id = login(UserDB, UserCursor)
#     print(user_id)
#     rating = rate_previous_experience()
#     add_rating_to_database(user_id, rating, UserDB, UserCursor)
# elif op.lower() == 'n':
#     user_id = register(UserDB, UserCursor)
#     print(user_id)
ids = RefineData(NiteDB, NiteCursor)
print(ids)
ProfileVectors = LoadRelevantVectors(ids, NiteCursor, NiteDB)
# d = preprocessing.normalize(w2v.GetWordVector('live').reshape(1,300))
# print('Profile vectors loaded') 
KeywordsToTry = ['lively', 'chic', 'electric', 'new', 'luxurious', 'expensive']
d = VectorisePreferences(KeywordsToTry)

scores = GetClosestVector(ProfileVectors, d)


print('Job complete:\n')
print("Best Score: ", scores[0])
print('\n')
i=1
for s in scores:
    print(str(i)+'.')
    print('Score:', s[0])
    PrintVenueRecord(ids[s[1]], NiteCursor, NiteDB)
    i=i+1
output_file("lines.html")

# p = figure(title="Vectors", x_axis_label='dim', y_axis_label='scale')
# p.line([f for f in range(300)], ProfileVectors[location].reshape(300), line_width=1, color="green", legend_label="Club Found")
# p.line([f for f in range(300)], d.reshape(300), line_width = 1, color = "red", legend_label = "live")
# show(p)
# vector = ProfileVectors[location]
# add_experience(user_id, UserDB, UserCursor, vector)



