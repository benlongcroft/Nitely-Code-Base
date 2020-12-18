# from gensim.models import Word2Vec
# from gensim.models.fasttext import FastText as FT_gensim
# def TrainWord2Vec(Data):
# 	model = Word2Vec(Data, size = 400, window = 4, min_count=1, workers=6, sg=1)
# 	return model

# def get_related_words(ActualWord, model):
# 	return model.wv.most_similar(positive=ActualWord)[:3]

# def GetWordVector(word, model):
# 	try:
# 		return model.wv[word]
# 	except KeyError:
# 		return None

import spacy
nlp = spacy.load("en_core_web_md")

def GetRelatedWords(word):
	word = nlp.vocab[word]
	queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
	# by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
	by_similarity = [[x.text, word.similarity(x)] for x in queries]
	by_similarity = sorted(by_similarity, key=lambda x:x[1], reverse = True)
	if by_similarity[0][0] == word:
		del by_similarity[0]
	return by_similarity[:3]

def GetWordVector(word):
	return nlp.vocab[word].vector