"""
Engine behind K2K algorithm. This turns keywords into vectors and reweights them.
This has been optimised using a transposition table
"""
import pickle
import spacy
import numpy as np
from sklearn import preprocessing

nlp = spacy.load('en_core_web_md', disable=['parser', 'tagger', 'ner'])

lexemes = []  # get lexemes from pickled file and load into lexemes
pickle_off = open("./vector_k2k/lexemes.pkl", "rb")
temp = pickle.load(pickle_off)
for v in temp:
    lexemes.append(nlp.vocab[v])
pickle_off.close()


# TODO: Work out the ideal .prob value to use and streamline this function

def get_related_words(word):
    """
    Uses spacy to get related words to origin word

    :param word: origin word. String format
    :return: list of 3 most similar words with their similarity via spacy to origin word
    """
    word = nlp.vocab[word]  # get nlp vocab object for word
    _queries = []
    for _vocab_obj in lexemes:
        if _vocab_obj.is_lower == word.is_lower:
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
"""
The above function is not neccessary currently as all the descriptions are  
lemmatised in the db according to this function 
"""
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
"""
Also not neccessary currently and outdated as TFIDF is not the best method for 
analysing word importance just word frequency 
"""


def convert_word_to_vector(word):
    """
    Converts word into usable vector

    :param word: string word
    :return: numpy matrix of size (1, 300) normalised
    """
    return preprocessing.normalize(nlp.vocab[word].vector.reshape(1, 300))
    # normalise nlp word vector to shape 300


def check_transposition_table(word, tbl):
    """
    Checks if word is in list of dictionaries

    :param word: word to check string
    :param tbl: our transposition table
    :return: returns words children
    """
    # simply checks if word is in list of dictionaries
    for dic in tbl:
        if word == list(dic.keys())[0]:
            return dic[word]


def add_to_transposition_table(object_to_add, file_path, tbl):
    """
    Adds a word to the transposition table

    :param object_to_add: our dictionary to add in format
    :param file_path: filepath to write table too
    :param tbl: our transposition table
    :return: n/a
    """
    # simply writes the updated transposition table to the file
    tbl.extend(object_to_add)
    obj = open(file_path, 'wb')
    pickle.dump(tbl, obj)
    obj.close()


def tree_creation(tree, words_to_add, scores_to_add,
                  level, level_max, all_words_in_tree,
                  transposition_file_path):
    """
    Generates user tree based on user preferences.

    :param tree: empty to begin with but as this a recursive operation this will grow with each
    call
    :param words_to_add: Words to add to the tree. Varies with each call but starts with the
    origin words and expands to include children defined by spacy
    :param scores_to_add: Again, similar to above. ATM, 1 for all to begin with
    :param level: current tree depth. This counts how many 'middles' the tree has
    :param level_max: tree depth to max out at
    :param all_words_in_tree: All the words in the tree
    :param transposition_file_path: path to transposition table
    :return: users tree of related words for K2K
    """
    next_gen_words = []  # words to add at next generation
    next_gen_scores = []  # scores to add at next generation
    all_words_in_tree.extend(words_to_add)
    # add initial words to all_words_in_tree so that we dont add duplicates

    transposition_file_obj = open(transposition_file_path, 'rb')
    try:
        tbl = pickle.load(transposition_file_obj)
    except EOFError:
        tbl = []
    transposition_file_obj.close()
    words_for_transpos = []
    # opens transpos file and gets table, also define list to add new words too
    for x, __ in enumerate(words_to_add):
        trans_pos_result = check_transposition_table(words_to_add[x], tbl)
        # get usable words from transpos table if exists

        if trans_pos_result is not None:
            # if transpos result exists, define usable words as the result
            usable_words = trans_pos_result

        else:  # if not in transpos table, then do the old fashioned way ;]
            related_words = get_related_words(words_to_add[x])  # get related words
            usable_words = []  # create list for those that are not duplicates
            for y in related_words:
                if not y[0] in all_words_in_tree:
                    if y[1] >= 1:  # if the score is above 1, make it 0.99 for simplicity sake
                        y[1] = 0.99
                    usable_words.append(list(y))  # add word and score to usable if not a duplicate
            word_parent_score = scores_to_add[x]
            for i, __ in enumerate(usable_words):
                usable_words[i][1] = usable_words[i][1] * word_parent_score
                # reweighs according to the parents score so that the scores are
                # holistic not just relevant to the node above
            words_for_transpos.append({words_to_add[x]: usable_words})
            # add to list of new words to add to transpos

        all_words_in_tree.extend([y[0] for y in usable_words])
        # add usable words to the list of all words in the tree
        if len(usable_words) != 0:  # if there are words in usable
            tree[words_to_add[x]] = [scores_to_add[x]]  # add word and score
            tree[words_to_add[x]].append(usable_words)
            # add the new words and scores to the node i.e creating new children
        next_gen_words.extend([y[0] for y in usable_words])
        # add the new usable words to the words to add on the next generation
        next_gen_scores.extend([y[1] for y in usable_words])  # same as above but with scores

    if level == level_max:  # refers to number of middle layers, if a complete...
        for y in next_gen_words:  # add the final words as final leaves
            tree[y] = [next_gen_scores[next_gen_words.index(y)]]
        return tree  # finish

    else:
        add_to_transposition_table(words_for_transpos, transposition_file_path, tbl)
        # add all new words to transpos file
        level = level + 1  # increment middle layer counter
        tree_creation(tree, next_gen_words, next_gen_scores,
                      level, level_max, all_words_in_tree, transposition_file_path)
        # call routine again with new words
        return tree  # for when complete


def turn_to_vector(tree):
    """
    Turns tree into multi-dimensional vector

    :param tree: Users tree as defined above
    :return: numpy matrix of (1,300) which is the users vector
    """
    total_vector = np.array([0 for x in range(300)])  # create blank vector
    for x in list(tree.keys()):  # go through every node
        parent = tree[x]  # get parents value
        parent_score = convert_word_to_vector(x) * float(parent[0])
        # turn parent into vector weighted on scalar product of its score to its own parent
        try:
            for child in parent[1]:  # for each child node in the parent
                parent_score = parent_score + (convert_word_to_vector(child[0]) * float(child[1]))
                # parent_score = parent_score + (child vector * child's relationship score)
            total_vector = total_vector + parent_score
            # once all children are processed, add to parent
        except IndexError:
            # if it is the final child then ignore as has
            # already been weighted when processing its parent
            pass
    return total_vector
