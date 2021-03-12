"""
Creates K2K class and calls essential functions to act on vectors to establish similarity
vectors should be pre-prepared. See NiteV1 for script to do so

"""
from scipy.spatial import distance
import numpy as np
from sklearn import preprocessing
from .create_vector import tree_creation, turn_to_vector
from sklearn import preprocessing


class K2K:
    """
    Class to establish user vectors and produce dataframes from users keywords so we can choose
    venues for the user and sort them in order of interest to user.
    """

    def __init__(self, keywords, weightings):
        self.__user_vector = self.convert_keywords_to_vectors(keywords, weightings)
        # gets user vector. Can take a while
        # depending on length of keywords list
        self.__user_vector = preprocessing.normalize(self.__user_vector)
        # normalise vector

    @property
    def get_user_vector(self):
        """
        :return: Users vector private numpy array size 300
        """
        return self.__user_vector

    @staticmethod
    def composite_vector(vectors):  # finds midpoint of list of vectors
        """
        Finds midpoint between list of vectors and normalises the result

        :param vectors: list of numpy vectors of size (1, 300)
        :return: normalised midpoint of vectors
        """
        composite_vector = np.array([0 for x in range(300)])
        for current_vector in vectors:
            composite_vector = np.add(current_vector, composite_vector)
        return preprocessing.normalize((composite_vector / len(vectors)).reshape(1, 300))

    @staticmethod
    def convert_keywords_to_vectors(keywords, weightings):
        """
        Converts a list of keywords into a 300 dimensional vector

        :param keywords: Users keywords in list
        :param weightings: weightings of keywords
        :return: vector of keywords and weightings
        """
        return turn_to_vector(tree_creation({},
                                            keywords,
                                            weightings,
                                            0, 1, [],
                                            './vector_k2k/transpositiontbl.pkl'))

    def get_closest_vectors(self, valid_venues_df, user_vector):
        """
        Gets vectors closest to user vector from df

        :param valid_venues_df: Pandas DataFrame of all valid venues
        :param user_vector: users numpy vector
        :return: sorted df by similarity to users vector
        """
        user_vector = user_vector.reshape(1, 300)
        _similarity = []
        for vector in valid_venues_df['vector']:
            vector = np.array([float(x) for x in vector[0].split(' ')]).reshape(1, 300)
            # split the string vector and convert to
            # numpy array of floats
            _cos = distance.euclidean(user_vector, vector)
            _similarity.append(_cos)
        valid_venues_df['similarity'] = _similarity
        valid_venues_df.sort_values(by=['similarity'], inplace=True,
                                    ignore_index=True, ascending=False)
        return valid_venues_df  # returns all vectors and their distances from the user_vector
