
# w = open('words.txt', 'r')
# words = [line.strip('\n') for line in w.readlines()]
# print(words)
import sqlite3
words = ['relaxed', 'relax', 'comfortable', 'calm', 'quiet', 'casual', 'pleasant', 'peaceful', 'gentle', 'mood', 'warm', 'intimate', 'pleasant', 'soft', 'mild', 'subtle']
def description_intensity(list_of_words):
    intensity = 0
    # TODO: actually make this accurate using proper techniques
    for word in list_of_words:
        if word.lower() in words:
            intensity=intensity+1
    intensity = 1-(intensity / len(list_of_words))
    return intensity

def check_venue_type(venue, cursor, venue_types):
    correct_type = False
    venue_id = venue['venue_id']
    # music_types = [1, 2, 3, 5, 6, 13, 15, 17, 18]
    # TODO: implement music_type command after
    command = '''SELECT venue_to_type.venue_type_id FROM venue_to_type WHERE venue_id == ?'''
    cursor.execute(command, (venue_id,))
    result = cursor.fetchall()
    for x in result:
        if x[0] in venue_types:
            correct_type = True
            break
    return correct_type
