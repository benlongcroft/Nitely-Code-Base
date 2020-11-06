import math
import spacy
import sqlite3
from matplotlib import pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

class WordMetaData:
    def __init__(self, data, numofdocs):
        self.data = data
        self.numberofdocs=numofdocs
    # def CheckExistence(self,ListToSearch):

    def SplitIntoWords(self, Passage):
        words = Passage.split(' ')
        return words

    def sentiment_analyzer_scores(self, word):
        score = analyser.polarity_scores(word)
        return score['compound']

    def tfidfscore(self):
        frequencys = {}
        sentiments = {}
        doc = 0
        for x in self.data:
            doc = doc+1
            x = x.split(' ')
            for word in x:
                try:
                    frequencys[word][0] == True
                    frequencys[word][0] = (frequencys[word][0]+1)
                    if frequencys[word][1][-1] != doc:
                        frequencys[word][1].append(doc)
                except:
                    frequencys[word] = [1, [doc]]
                sentiments[word] = self.sentiment_analyzer_scores(word)
        tf_idf = {}
        tfs = []
        idfs = []
        for key in frequencys.keys():
            freq_in_text = frequencys[key][0]
            document_frequency= len(frequencys[key][1])
            tf = freq_in_text
            idf = math.log(self.numberofdocs/document_frequency)
            if key != '\n':
                tf_idf[key] = [tf*idf]
            tfs.append(tf)
            idfs.append(idf)
        self.tf_idf = tf_idf

        return tf_idf, sentiments
