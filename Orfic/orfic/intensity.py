
words = ['relaxed', 'relax', 'comfortable', 'calm', 'quiet', 'casual', 'pleasant', 'peaceful', 'gentle', 'mood', 'warm', 'intimate', 'pleasant', 'soft', 'mild', 'subtle']
def description_intensity(list_of_words):
    intensity = 0
    # TODO: actually make this accurate using proper techniques
    for word in list_of_words:
        if word.lower() in words:
            intensity=intensity+1
    intensity = (intensity / len(list_of_words))
    return intensity

def check_venue_music_type(venue, cursor, applicable_venue_types, applicable_music_types):
    correct_music = False
    correct_venue = False
    venue_id = venue['venue_id']

    venue_command = '''SELECT venue_to_type.venue_type_id FROM venue_to_type WHERE venue_id == ?'''
    music_command = '''SELECT venue_genres.genre_id FROM venue_genres WHERE venue_genres.venue_id = ?'''

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
    if correct_venue and correct_music:
        return True
    else:
        return False
