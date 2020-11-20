import numpy as np
from sklearn import preprocessing
import spacy
import pickle
from time import perf_counter

t1_start = perf_counter()
nlp = spacy.load('en_core_web_md', disable=['parser', 'tagger', 'ner'])

lexemes = []  # get lexemes from pickled file and load into lexemes
pickle_off = open("./K2K/lexemes.pkl", "rb")
temp = pickle.load(pickle_off)
for v in temp:
    lexemes.append(nlp.vocab[v])
pickle_off.close()
# TODO: Work out the ideal .prob value to use and streamline this function

# lexemes = []
# if nlp.vocab.lookups_extra.has_table("lexeme_prob"):
#     nlp.vocab.lookups_extra.remove_table("lexeme_prob")
# #
# for orth in nlp.vocab.vectors:
#     if nlp.vocab[orth].prob >= -12:
#         lexemes.append(nlp.vocab[orth])

t1_stop = perf_counter()  # time it
print("Elapsed time:", t1_stop, t1_start)
print("Action took in seconds:", t1_stop - t1_start)


def GetRelatedWords(word):
    word = nlp.vocab[word]  # get nlp vocab object for word
    _queries = []
    for _vocab_obj in lexemes:
        if _vocab_obj.is_lower:
            _queries.append(_vocab_obj)
    by_similarity = [[x.text, x.similarity(word)] for x in _queries]  # find similarity
    by_similarity = sorted(by_similarity, key=lambda x: x[1], reverse=True)  # sort similarity
    if by_similarity[0][0] == word:  # if first word in by_similarity is the origin word, delete it
        del by_similarity[0]
    return by_similarity[:3]  # return three most similar words


# def LemmatiseProfile(Profile):
#     lemmatised_profile = nlp(Profile)
#     profile_lemmas = []
#     for word in lemmatised_profile:
#         if not word.is_punct | word.is_stop:
#             if word.pos_ == 'ADJ':
#                 profile_lemmas.append(word.lemma_)
#     if len(profile_lemmas) != 0:
#         return profile_lemmas
#     else:
#         return 'Error, profile has no values in it or no ability to create lemmas of words'

'''The above function is not neccessary currently as all the descriptions are lemmatised in the db according to this 
function '''
# TODO: do some more research on finding the most important words in a description

# def GetKeywords(profile, TfidfScores):
#     keywords = []
#     profile = profile.split(' ')
#     for token in profile:
#         try:
#             if token == '\n' or token == '':
#                 continue
#             else:
#                 keywords.append([token, TfidfScores[token]])
#         except KeyError:
#             print('Word not in Dictionary')
#     keywords = sorted(keywords, key=lambda x: x[1])
#     for x in range(len(keywords)):
#         keywords[x][1] = 1
#     return keywords[:10]
'''Also not neccessary currently and outdated as TFIDF is not the best method for analysing word importance just word 
frequency '''


def ConvertWordToVector(word):
    return preprocessing.normalize(nlp.vocab[word].vector.reshape(1, 300))  # normalise nlp word vector to shape 300


def CheckTranspositionTable(word, tbl):
    # simply checks if word is in list of dictionaries
    for dic in tbl:
        if word == list(dic.keys())[0]:
            return dic[word]


def AddToTranspositionTable(object_to_add, FilePath, tbl):
    # simply writes the updated transposition table to the file
    tbl.extend(object_to_add)
    obj = open(FilePath, 'wb')
    pickle.dump(tbl, obj)
    obj.close()


def TreeCreation(Tree, WordsToAdd, ScoresToAdd, level, LevelMax, AllWordsInTree, TranspositionFilePath):
    next_gen_words = []  # words to add at next generation
    next_gen_scores = []  # scores to add at next generation
    AllWordsInTree.extend(WordsToAdd)  # add inital words to AllWordsInTree so that we dont add duplicates

    transposition_file_obj = open(TranspositionFilePath, 'rb')
    tbl = pickle.load(transposition_file_obj)
    transposition_file_obj.close()
    words_for_transpos = []
    # opens transpos file and gets table, also define list to add new words too
    for x in range(len(WordsToAdd)):
        trans_pos_result = CheckTranspositionTable(WordsToAdd[x], tbl)  # get usable words from transpos table if exists

        if trans_pos_result is not None:  # if transpos result exists, define usable words as the result
            usable_words = trans_pos_result

        else:  # if not in transpos table, then do the old fashioned way ;]
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
            words_for_transpos.append({WordsToAdd[x]: usable_words})  # add to list of new words to add to transpos

        AllWordsInTree.extend([y[0] for y in usable_words])  # add usable words to the list of all words in the tree
        if len(usable_words) != 0:  # if there are words in usable
            Tree[WordsToAdd[x]] = [ScoresToAdd[x]]  # add word and score
            Tree[WordsToAdd[x]].append(usable_words)
            # add the new words and scores to the node i.e creating new children
        next_gen_words.extend([y[0] for y in usable_words])
        # add the new usable words to the words to add on the next generation
        next_gen_scores.extend([y[1] for y in usable_words])  # same as above but with scores

    if level == LevelMax:  # refers to number of middle layers, if a complete...
        for y in next_gen_words:  # add the final words as final leaves
            Tree[y] = [next_gen_scores[next_gen_words.index(y)]]
        return Tree  # finish

    else:
        AddToTranspositionTable(words_for_transpos, TranspositionFilePath, tbl)  # add all new words to transpos file
        level = level + 1  # increment middle layer counter
        TreeCreation(Tree, next_gen_words, next_gen_scores, level, LevelMax, AllWordsInTree, TranspositionFilePath)
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
