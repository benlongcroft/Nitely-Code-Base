import Word2Vec as w2v
import spacy
import numpy as np
def Sort2DList(BestMatchs):
        BestMatchs = sorted(BestMatchs, key=lambda x:x[1])
        return BestMatchs

nlp = w2v.nlp

def LemmatiseProfile(Profile):
    LProfile = nlp(Profile)
    d=[]
    for x in LProfile:
        if not x.is_punct | x.is_stop:
            if x.pos_ == 'ADJ':
                d.append(x.lemma_)
    if len(d) != 0:
        return d
    else:
        return 'Error'

def GetKeywords(profile, TfidfScores, SentimentScores):
        Keywords = []
        profile = profile.split(' ')
        for token in profile:
            try:
                if token == '\n' or token == '':
                    continue
                else:
                    Keywords.append([token, TfidfScores[token]])
            except KeyError:
                print('Word not in Dictionary')
        Keywords = Sort2DList(Keywords)
        for x in range(len(Keywords)):
            Keywords[x][1] = 1
        return Keywords[:10]

def RecursiveTreeCreation(Tree, WordsToAdd, ScoresToAdd, Level, LevelMax, AllWordsInTree):
    NextGenWords = [] #words to add at next generation
    NextGenScores = [] # scores to add at next generation
    AllWordsInTree.extend(WordsToAdd) #add inital words to AllWordsInTree so that we dont add duplicates
    for x in range(len(WordsToAdd)):
        Tree[WordsToAdd[x]] = [ScoresToAdd[x]] #add word and score
        RelatedWords = w2v.GetRelatedWords(WordsToAdd[x]) #get related words
        Usable = [] #create list for those that are not duplicates
        for y in RelatedWords:
            if not y[0] in AllWordsInTree:
                if y[1] >= 1: #if the score is above 1, make it 0.99 for simplicity sake
                    y[1] = 0.99
                Usable.append(list(y)) #add word and score to usable if not a duplicate
        ParentScore = ScoresToAdd[x]
        for i in range(len(Usable)):
            Usable[i][1] = Usable[i][1]*ParentScore 
            #reweights according to the parents score so that the scores are holistic not just relevant to the node above
        AllWordsInTree.extend([y[0] for y in Usable]) #add usable words to the list of all words in the tree
        if len(Usable) != 0: #if there are words in usable
            Tree[WordsToAdd[x]].append(Usable) #add the new words and scores to the node i.e creating new children
        NextGenWords.extend([y[0] for y in Usable]) #add the new usable words to the words to add on the next generation
        NextGenScores.extend([y[1] for y in Usable]) #same as above but with scores
    if Level == LevelMax: #refers to number of middle layers, if a complete...
        for y in NextGenWords: #add the final words as final leaves
            Tree[y] = [NextGenScores[NextGenWords.index(y)]]
        return Tree #finish
    else:
        Level = Level+1 #increment middle layer counter
        RecursiveTreeCreation(Tree, NextGenWords, NextGenScores, Level, LevelMax, AllWordsInTree) #call routine again with new words
        return Tree #for when complete

def TurnToVector(Tree):
    TotalVector = np.array([0 for x in range(300)]) #create blank vector 
    for x in list(Tree.keys()): #go through every node
        Parent = Tree[x] #get parents value 
        ParentScore = w2v.GetWordVector(x) * float(Parent[0]) 
        #turn parent into vector weighted on scalar product of its score to its own parent
        try:
            for child in Parent[1]: #for each child node in the parent
                ParentScore = ParentScore + (w2v.GetWordVector(child[0]) * float(child[1])) 
                #parentscore = parentscore + (child vector * childs relationship score)
            TotalVector = TotalVector + ParentScore #once all children are processed, add to parent
        except IndexError: 
            #if it is the final child then ignore as has already been weighted when processing its parent
            pass
    return TotalVector