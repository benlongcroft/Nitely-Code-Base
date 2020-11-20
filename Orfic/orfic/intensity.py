
words = ['relaxed', 'relax', 'comfortable', 'calm', 'quiet', 'casual', 'pleasant', 'peaceful', 'gentle', 'mood', 'warm', 'intimate', 'pleasant', 'soft', 'mild', 'subtle']
def description_intensity(list_of_words):
    intensity = 0
    # TODO: actually make this accurate using proper techniques
    for word in list_of_words:
        if word.lower() in words:
            intensity=intensity+1
    intensity = (intensity / len(list_of_words))
    return intensity

#TODO: Also fix this piece of shit while you are at it
def check_venue_music_type(venue, cursor, applicable_venue_types, applicable_music_types, df, other_args):
    i = 1
    while True:
        correct_music = False
        correct_venue = False
        venue_id = venue['venue_id']

        venue_command = '''SELECT venue_to_type.venue_type_id FROM venue_to_type, venues WHERE venue_to_type.venue_id == ?'''
        music_command = '''SELECT venue_genres.genre_id FROM venue_genres, venues WHERE venue_genres.venue_id = ?'''
        if other_args != None:
            venue_command = venue_command + other_args
            music_command = music_command + other_args
        cursor.execute(venue_command, (venue_id,))
        venue_types = [x[0] for x in cursor.fetchall()]

        cursor.execute(music_command, (venue_id,))
        music_types = [x[0] for x in cursor.fetchall()]

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
                i = i+1
            else:
                return None
