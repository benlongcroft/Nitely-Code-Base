"""
Analyses intensity of venue to establish whether it is ideal for its position in the night
"""


# words = ['relaxed', 'relax', 'comfortable', 'calm', 'quiet', 'casual', 'pleasant', 'peaceful',
#          'gentle', 'mood', 'warm', 'intimate', 'pleasant', 'soft', 'mild', 'subtle']


# def description_intensity(list_of_words):
#     """
#
#     :param list_of_words: Words to check against
#     :return:
#     """
#     intensity = 0
#     # TODO: actually make this accurate using proper techniques
#     for word in list_of_words:
#         if word.lower() in words:
#             intensity = intensity + 1
#     intensity = (intensity / len(list_of_words))
#     return intensity

def venue_type(venue, cursor, applicable_venue_types, df):
    origin = venue
    i = 1
    while True:
        venue_id = venue['venue_id']
        venue_command = '''SELECT venue_to_type.venue_type_id FROM venue_to_type, venues WHERE 
        venue_to_type.venue_id == ? AND venue_to_type.venue_id = venues.venue_id'''
        cursor.execute(venue_command, (venue_id,))
        venue_types = [x[0] for x in cursor.fetchall()]
        for t in venue_types:
            if t in applicable_venue_types:
                return venue
            else:
                if i == len(df):
                    print('Chose original')
                    return origin
                else:
                    venue = df.iloc[i]
                    i = i + 1


def check_venue_music_type(venue, cursor, applicable_venue_types, applicable_music_types, df,
                           other_args):
    """
    checks whether venue type and music type is good for current pos in night

    :param venue: venue to check (panda record)
    :param cursor: db cursor. SQLITE3 obj
    :param applicable_venue_types: types of venues we are looking for (list)
    :param applicable_music_types: types of music we are looking for (list)
    :param df: Pandas DataFrame of all valid venues
    :param other_args: any other args we want
    :return: the correct venue as pandas record
    """
    i = 1
    while True:
        correct_music = False
        correct_venue = False
        venue_id = venue['venue_id']

        venue_command = '''SELECT venue_to_type.venue_type_id FROM venue_to_type, venues 
                           WHERE venue_to_type.venue_id == ?'''
        music_command = '''SELECT venue_genres.genre_id FROM venue_genres, venues 
                           WHERE venue_genres.venue_id = ?'''
        if other_args is not None:
            venue_command = venue_command + other_args
            music_command = music_command + other_args
        cursor.execute(venue_command, (venue_id,))
        venue_types = [x[0] for x in cursor.fetchall()]

        cursor.execute(music_command, (venue_id,))
        music_types = [x[0] for x in cursor.fetchall()]
        print(music_types)
        print(venue_types)
        for m_type in music_types:
            if m_type in applicable_music_types:
                correct_music = True
                break

        for v_type in venue_types:
            if v_type in applicable_venue_types:
                correct_venue = True
                break

        if correct_music and correct_venue:
            return venue
        else:
            if i < len(df):
                venue = df.iloc[i]
                i = i + 1
                print('New venue: ', venue['name'])
                print('going round again')
            else:
                return None
