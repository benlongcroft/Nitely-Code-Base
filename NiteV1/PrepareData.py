import sqlite3
import TreeCreation as TC

def MakeList(path):
    q = open(path, "r")
    r = q.readlines()
    t = []
    punct = '''.,"/()\|':'''
    for e in r:
        e = e.strip()
        e = e.lower()
        nopunct = ""
        for x in e:
            if x not in punct:
                nopunct = nopunct + x
        t.append(nopunct)
    return t

def CreateDatabase(path):
    NiteDB = sqlite3.connect('/Users/benlongcroft/Documents/Nite/ClubDataDB.db')
    cursor = NiteDB.cursor()
    cursor.execute('''CREATE TABLE venues([venue_id] INTEGER PRIMARY KEY, 
                                            [name] varchar(500), 
                                            [description] varchar(10000), 
                                            [venue_type] varchar(100), 
                                            [age_restriction] varchar(100),
                                            [entry_price] varchar(200),
                                            [dress_code] varchar(200),
                                            [dress_rating] INTEGER)''')
    NiteDB.commit()
    extensions = ["AgeRestrictions", "DressCode", "EntryPrice", "MusicType", "VenueType"]

    AllNames = MakeList(path+'.txt')
    AllDescriptions = []
    AllAgeRestrictions = MakeList(path+"AgeRestrictions"+'.txt')
    AllDressCodes = MakeList(path+"DressCode"+'.txt')
    AllEntryPrices = MakeList(path+"EntryPrice"+'.txt')
    AllDressRatings = MakeList(path+"DressCodeRatings"+'.txt')

    Descriptions = open((path+"Descriptions"+'.txt'), "r")
    ReadData = Descriptions.readlines()

    for x in ReadData:
        AllDescriptions.append(' '.join(TC.LemmatiseProfile(x)))
    Descriptions.close()

    command = ('''INSERT INTO venues (name, description, age_restriction, entry_price, dress_code, dress_rating) VALUES (?, ?, ?, ?, ?, ?)''')

    for x in range(len(AllDressCodes)):
        values = [AllNames[x], AllDescriptions[x], AllAgeRestrictions[x], AllEntryPrices[x], AllDressCodes[x], AllDressRatings[x]]
        cursor.execute(command, values)
    NiteDB.commit()
    return cursor, NiteDB
# CreateDatabase("/Users/benlongcroft/Documents/Nite/ClubData/AllLondonClubs")