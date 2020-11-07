import spacy
from scipy.spatial import distance
import pandas as pd
from sklearn import preprocessing

nlp = spacy.load("en_core_web_md")


# vectors should be pre-prepared. See NiteV1 for script to do so

def ConvertWordToVector(word):
    return preprocessing.normalize(nlp.vocab[word].vector.reshape(1, 300))  # normalise nlp word vector to shape 300


def ConvertKeywordsToVectors(keywords, weightings):
    return TC.TurnToVector(TC.RecursiveTreeCreation({}, keywords, weightings, 0, 1, []))


def GetClosestVectors(all_venue_vectors, user_vector):
    user_vector = user_vector.reshape(1, 300)
    vectors_df = pd.DataFrame(columns=["vector", "distance"])
    for i in range(len(all_venue_vectors)):
        v = all_venue_vectors[i]
        cos = distance.euclidean(user_vector, v.reshape(1, 300))
        # must reshape numpy array to numpy matrix
        # TODO: This gets the euclidian distance between two vectors, maybe consider other metrics?
        vectors_df.append({"vector": v, 'distance': cos}, ignore_index=True)
    vectors_df.sort_values(by=['distance'], inplace=True)
    return vectors_df  # returns all vectors and their distances from the user_vector
