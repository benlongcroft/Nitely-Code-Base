from .main import nlp, ConvertWordToVector
import numpy as np


def Sort2DList(BestMatchs):
    return sorted(BestMatchs, key=lambda x: x[1])


def LemmatiseProfile(Profile):
    lemmatised_profile = nlp(Profile)
    profile_lemmas = []
    for word in lemmatised_profile:
        if not word.is_punct | word.is_stop:
            if word.pos_ == 'ADJ':
                profile_lemmas.append(word.lemma_)
    if len(profile_lemmas) != 0:
        return profile_lemmas
    else:
        return 'Error, profile has no values in it or no ability to create lemmas of words'


def GetKeywords(profile, TfidfScores):
    keywords = []
    profile = profile.split(' ')
    for token in profile:
        try:
            if token == '\n' or token == '':
                continue
            else:
                keywords.append([token, TfidfScores[token]])
        except KeyError:
            print('Word not in Dictionary')
    keywords = Sort2DList(keywords)
    for x in range(len(keywords)):
        keywords[x][1] = 1
    return keywords[:10]


def TreeCreation(Tree, WordsToAdd, ScoresToAdd, Level, LevelMax, AllWordsInTree):
    next_gen_words = []  # words to add at next generation
    next_gen_scores = []  # scores to add at next generation
    AllWordsInTree.extend(WordsToAdd)  # add inital words to AllWordsInTree so that we dont add duplicates
    for x in range(len(WordsToAdd)):
        Tree[WordsToAdd[x]] = [ScoresToAdd[x]]  # add word and score
        related_words = GetRelatedWords(WordsToAdd[x])  # get related words
        usable_words = []  # create list for those that are not duplicates
        for y in related_words:
            if not y[0] in AllWordsInTree:
                if y[1] >= 1:  # if the score is above 1, make it 0.99 for simplicity sake
                    y[1] = 0.99
                usable_words.append(list(y))  # add word and score to usable if not a duplicate
        word_parent_score = ScoresToAdd[x]
        for i in range(len(usable_words)):
            usable_words[i][1] = usable_words[i][1] * word_parent_score
            # reweighs according to the parents score so that the scores are holistic not just relevant to the node
            # above
        AllWordsInTree.extend([y[0] for y in usable_words])  # add usable words to the list of all words in the tree
        if len(usable_words) != 0:  # if there are words in usable
            Tree[WordsToAdd[x]].append(usable_words)
            # add the new words and scores to the node i.e creating new children
        next_gen_words.extend([y[0] for y in usable_words])
        # add the new usable words to the words to add on the next generation
        next_gen_scores.extend([y[1] for y in usable_words])  # same as above but with scores
    if Level == LevelMax:  # refers to number of middle layers, if a complete...
        for y in next_gen_words:  # add the final words as final leaves
            Tree[y] = [next_gen_scores[next_gen_words.index(y)]]
        return Tree  # finish
    else:
        Level = Level + 1  # increment middle layer counter
        TreeCreation(Tree, next_gen_words, next_gen_scores, Level, LevelMax,AllWordsInTree)
        # call routine again with new words
        return Tree  # for when complete


def TurnToVector(Tree):
    total_vector = np.array([0 for x in range(300)])  # create blank vector
    for x in list(Tree.keys()):  # go through every node
        parent = Tree[x]  # get parents value
        parent_score = ConvertWordToVector(x) * float(parent[0])
        # turn parent into vector weighted on scalar product of its score to its own parent
        try:
            for child in parent[1]:  # for each child node in the parent
                parent_score = parent_score + (ConvertWordToVector(child[0]) * float(child[1]))
                # parent_score = parent_score + (child vector * child's relationship score)
            total_vector = total_vector + parent_score  # once all children are processed, add to parent
        except IndexError:
            # if it is the final child then ignore as has already been weighted when processing its parent
            pass
    return total_vector
