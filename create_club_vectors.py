import sqlite3
from K2K.main import K2K
from math import log
from statistics import stdev
from time import perf_counter


class weighting_object:
    def __init__(self, corpus):
        '''
        Initialising of weighting object which will determine weight of words
        in description

        :param corpus: list of sets
        '''
        self.tf_dictionary = {}
        self.idf_dictionary = {}
        self.__dictionary = {}
        self.corpus = corpus
        self.number_of_documents = len(self.corpus)
        self.__magic_words = {'food', 'theme', 'dj', 'beer', 'brunch', 'traditional',
                              'cocktails', 'terrace', 'live', 'wine', 'sports', 'gay',
                              'bar', 'pub', 'club', 'other'}
        self.magic_word_value = 0.5

    @property
    def magic_words(self):
        '''
        get magic words from object
        :return: magic words in dictionary
        '''
        return self.__magic_words

    @magic_words.setter
    def magic_words(self, new_words):
        '''
        set magic words for object
        :param new_words: set of words to set as new magic words
        '''
        self.__magic_words = new_words

    @staticmethod
    def weight_tf_dictionary(dictionary, k):
        """
        Weights the term frequency according to k normalisation
        :param dictionary:
        :param k: k value for normalisation
        :return: dictionary of re-weighted terms
        """
        highest_frequency_word = max(dictionary.values())
        keys = list(dictionary.keys())
        for i, __ in enumerate(keys):
            dictionary[keys[i]] = k + k * (dictionary[keys[i]] / highest_frequency_word)

        return dictionary

    @property
    def term_frequency(self):
        """
        calculate term frequency for each term in dictionary
        :return: normalised dictionary of term frequencies
        """
        dictionary = {}
        for document in self.corpus:
            for word in document:
                word = word.lower()
                if word in self.__magic_words or word == '':  # removes magic words from dictionary
                    continue
                else:
                    if word in dictionary:
                        dictionary[word] = dictionary[word] + 1
                    else:
                        dictionary[word] = 1

        return self.weight_tf_dictionary(dictionary, 0.5)

    def count_document_frequency(self, word):
        count = 0
        for document in self.corpus:
            if word in document:
                count += 1
                continue
        return count

    def inverse_document_frequency(self, tf_dictionary):
        dictionary = {}
        for word in tf_dictionary.keys():
            if word in self.__magic_words:
                continue
            else:
                df = self.count_document_frequency(word)
                dictionary[word] = log((self.number_of_documents - df + 0.5) / (df + 0.5) + 1)
        return dictionary

    def normalise_tfidf(self, dictionary):
        d_mean = sum(dictionary.values())/len(dictionary)
        d_stdev = stdev(dictionary.values())
        for word, score in dictionary.items():
            dictionary[word] = (score - d_mean)/d_stdev
        return dictionary


    @property
    def populate_dictionary(self):
        """Populates dictionary from corpus of text
        :return: normalised dictionary of term frequencies"""
        self.tf_dictionary = self.term_frequency
        self.idf_dictionary = self.inverse_document_frequency(self.tf_dictionary)
        for word in self.tf_dictionary.keys():
            self.__dictionary[word] = self.tf_dictionary[word] * self.idf_dictionary[word]
        print(
            {key: val for key, val in sorted(self.tf_dictionary.items(), key=lambda ele: ele[1])})
        print(
            {key: val for key, val in sorted(self.idf_dictionary.items(), key=lambda ele: ele[1])})
        for word in self.__magic_words:
            # adds magic words with slightly higher tf_idf value so that
            # more similar venues 'clump' together as the vectors will be closer
            # alter the magic_word_value to increase/decrease the affect of the magic
            # words on the vectors
            self.__dictionary[word] = 1
        # self.__dictionary = self.normalise_tfidf(self.__dictionary)
        return self.__dictionary


db = sqlite3.connect('/Users/benlongcroft/Documents/Nitely Project/NewDB/ExperimentalOrficDB.db')
cur = db.cursor()

cur.execute('''SELECT description, type FROM venue_info WHERE description != "DO NOT USE"''')
descriptions = []
for item in cur.fetchall():
    des = item[0].split(', ')
    des.append(item[1])
    descriptions.append(list(set(des)))

# descriptions = [list(set(x[0].split(', '))) for x in cur.fetchall()]
print(descriptions)
weightings = weighting_object(descriptions).populate_dictionary
res = {key: val for key, val in sorted(weightings.items(), key=lambda ele: ele[1])}
print(res)
done = 0
club_vectors_total = []
time_taken = []
for d in descriptions:
    if d[0] == 'DO NOT USE':
        continue
    else:
        t1_start = perf_counter()
        # w = [weightings[word.lower()] for word in d]
        k = K2K(d, [1 for x in range(len(d))])
        print(d)
        club_vectors_total.append(k.get_user_vector)

        done = done + 1
        t2_end = perf_counter()
        time_taken.append(t2_end - t1_start)
        seconds_total = (sum(time_taken) / len(time_taken)) * (len(descriptions) - done)
        print('Total time remaining in seconds:', seconds_total)

from bokeh.plotting import figure, output_file, show
import random
import pickle
with open('club_vectors_31-01-2021.txt', 'wb') as fh:
   pickle.dump(club_vectors_total, fh)

output_file("lines.html")
p = figure(title="Vectors", x_axis_label='dim', y_axis_label='scale')
r = lambda: random.randint(0, 255)
for d in club_vectors_total:
    col = ('#%02X%02X%02X' % (r(), r(), r()))
    p.line([f for f in range(300)], d.reshape(300), line_width=1, color=col, legend_label="live")
show(p)
# TODO: 'Need food, Text FOOD to this number to make your next location snackable!' using food tag
# TODO: Create a 'some of our favourites section' which are handpicked routes through newcastle - delegate to Hugo?
