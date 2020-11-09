from scipy.spatial import distance
from .CreateVector import TreeCreation, TurnToVector, GetRelatedWords
import numpy as np

# vectors should be pre-prepared. See NiteV1 for script to do so

class K2K:
    def __init__(self, df, keywords, weightings):
        self.__user_vector = self.ConvertKeywordsToVectors(keywords, weightings)
        self.__df = self.GetClosestVectors(df, self.__user_vector)

    @property
    def get_user_vector(self):
        return self.__user_vector

    @property
    def get_df(self):
        return self.__df

    def ConvertKeywordsToVectors(self, keywords, weightings):
        return TurnToVector(TreeCreation({}, keywords, weightings, 0, 1, []))

    def GetClosestVectors(self, valid_venues_df, user_vector):
        user_vector = user_vector.reshape(1, 300)
        _similarity = []
        for v in valid_venues_df['vector']:
            v = np.array([float(x) for x in v[0].split(' ')]).reshape(1, 300) #split the string vector and convert to numpy array of floats
            _cos = distance.euclidean(user_vector, v)
            # TODO: This gets the euclidian distance between two vectors, maybe consider other metrics?
            _similarity.append(_cos)
        valid_venues_df['similarity'] = _similarity
        return valid_venues_df  # returns all vectors and their distances from the user_vector
