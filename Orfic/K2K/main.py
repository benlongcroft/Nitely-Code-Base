from scipy.spatial import distance
from .CreateVector import TreeCreation, TurnToVector, GetRelatedWords
import numpy as np
from . import intensity

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

    def CompositeVector(self, x_vector, y_vector):
        return (x_vector + y_vector) / 2

    def ConvertKeywordsToVectors(self, keywords, weightings):
        return TurnToVector(TreeCreation({}, keywords, weightings, 0, 1, []))

    def GetClosestVectors(self, valid_venues_df, user_vector):
        user_vector = user_vector.reshape(1, 300)
        _similarity = []
        for v in valid_venues_df['vector']:
            v = np.array([float(x) for x in v[0].split(' ')]).reshape(1,
                                                                      300)  # split the string vector and convert to numpy array of floats
            _cos = distance.euclidean(user_vector, v)
            # TODO: This gets the euclidian distance between two vectors, maybe consider other metrics?
            _similarity.append(_cos)
        valid_venues_df['similarity'] = _similarity
        valid_venues_df.sort_values(by=['similarity'], inplace=True,
                                    ignore_index=True)
        return valid_venues_df  # returns all vectors and their distances from the user_vector

    def TestIntensity(self, values, expected):
        one = False
        for x in values:
            if x[0] in expected:
                    one = True
                    break
        return one

    def ReorderForIntensity(self, df, venue, position_in_night, total_venues, cursor):
        og = venue
        if position_in_night == 1:
            if (intensity.check_venue_type(venue, cursor, [2, 4, 5, 7, 9])) == False:
                for index, row in df.iterrows():
                    if (intensity.check_venue_type(row, cursor, [2, 4, 5, 7, 9])):
                        venue = row
                        break

        elif position_in_night == total_venues:
            if intensity.check_venue_type(venue, cursor, [1, 6, 8, 11]) == False:
                for index, row in df.iterrows():
                    if (intensity.check_venue_type(row, cursor, [1, 6, 8, 11])):
                        venue = row
                        break
        if og['venue_id'] != venue['venue_id']:
            print('Venue Changed!')
            print(og['name'],'-->', venue['name'])
        return venue
