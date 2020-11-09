from scipy.spatial import distance
from .CreateVector import TreeCreation, TurnToVector, GetRelatedWords


# vectors should be pre-prepared. See NiteV1 for script to do so

class K2K:
    def __init__(self, df, keywords, weightings):
        # user_tree = self.ConvertKeywordsToVectors(keywords, weightings)
        for x in keywords:
            print(GetRelatedWords(x))
        # TODO: rejig this so that K2K is actually accurate in returning a pandas df with the match of each venue
        # print(user_tree)

    def ConvertKeywordsToVectors(self, keywords, weightings):
        return TurnToVector(TreeCreation({}, keywords, weightings, 0, 1, []))

    def GetClosestVectors(self, valid_venues_df, user_vector):
        user_vector = user_vector.reshape(1, 300)
        _similarity = []
        for v in valid_venues_df['vector']:
            _cos = distance.euclidean(user_vector, v.reshape(1, 300))
            # must reshape numpy array to numpy matrix
            # TODO: This gets the euclidian distance between two vectors, maybe consider other metrics?
            _similarity.append(_cos)
        valid_venues_df['similarity'] = _similarity
        return valid_venues_df  # returns all vectors and their distances from the user_vector
