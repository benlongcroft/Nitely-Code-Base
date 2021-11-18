import random
from sklearn.manifold import TSNE
import sqlite3
import pickle
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, show
import spacy
import numpy as np


def group(types, vectors):
    all_types = {'pub': '000', 'bar': '001', 'club': '010', 'other': '011', 'live': '100'}
    # we convert the tag to a 3 bit tag and append restaurant and club bits to the end
    validation_data = {}
    grouping = {}
    i=0
    for venue in types:
        if (venue[1] is None) or (venue[2] is None):
            continue
        vector = vectors[i]
        i=i+1
        name = venue[0]
        type = venue[1].lower()
        restaurant = str(venue[2])
        club = str(venue[3])
        code = all_types[type] + restaurant + club

        validation_data[name] = code
        if code in grouping.keys():
            grouping[code].append({name:vector})
        else:
            grouping[code] = [{name:vector}]

    return grouping


def main():
    db_obj = sqlite3.connect(
        '/Users/benlongcroft/Documents/Nitely Project/Nitely/VENUES.db')
    cursor_obj = db_obj.cursor()

    pickle_off = open("/Users/benlongcroft/Documents/Nitely Project/Nitely/club_vectors_pkl/club_vectors_1-0.75.txt", "rb")
    vectors = pickle.load(pickle_off)
    print(vectors)
main()
    # vectors = [x[0] for x in vectors]
    #
    # command = '''SELECT name, tag, restaurant, club FROM venue_info'''
    # cursor_obj.execute(command)
    # group_tags = group(cursor_obj.fetchall(), vectors)
    #
    #
    # colors = brewer["Spectral"][len(group_tags)]
    # key_text = {'01001': 'Club + Club', '00101': 'Bar + Club', '00100': 'Bar',
    #             '00110': 'Bar + Restaurant', '00000': 'Pub', '00111': 'Bar + Restaurant + Club',
    #             '00010': 'Pub + Restaurant', '01100': 'Other', '10000': 'Live',
    #             '00011': 'Pub + Restaurant + Club'}
    # i = 0
    # map = []
    # col_tag = []
    # names=[]
    # vectors = []
    #
    # for key in group_tags:
    #     value = group_tags[key]
    #     for name in value:
    #         k = list(name.keys())[0]
    #         if k in venues_to_add.get_names():
    #             print(k, name[k])
    #             col_tag.append('Venues')
    #             map.append('blue')
    #             names.append(k)
    #             vectors.append(name[k].reshape(300))
    #         else:
    #             col_tag.append(key_text[key])
    #             map.append(colors[i])
    #             names.append(k)
    #             vectors.append(name[k].reshape(300))
    #     i = i + 1
    #
    #
    # col_tag.append('USERVEC')
    # map.append('red')
    # vectors.append(user_vec.reshape(300))
    # names.append('USERS VECTOR')
    #
    # NLP = spacy.load('en_core_web_md')
    # word = NLP.vocab['dj']
    # col_tag.append('WORD')
    # names.append('DJ WORD')
    # map.append('red')
    # vectors.append(np.array(word.vector).reshape(300))
    #
    # # cursor_obj.execute('''SELECT name FROM venue_info  WHERE description != 'DO NOT USE';''')
    # # names = [x[0] for x in cursor_obj.fetchall()]
    #
    # tsne = TSNE(perplexity=30, n_components=2, init='pca', early_exaggeration=7, learning_rate=100,
    #             n_iter=3000, n_iter_without_progress=1000, random_state=23)
    #
    # new_values = tsne.fit_transform(vectors)
    #
    # x = []
    # y = []
    # for value in new_values:
    #     x.append(value[0])
    #     y.append(value[1])
    # r = {'x_values': x, 'y_values': y, 'tags': names, "color": map, 'col_tag': col_tag}
    # source = ColumnDataSource(
    #     pd.DataFrame(r, columns=['x_values', 'y_values', 'tags', 'color', 'col_tag']))
    #
    # output_file("TSNE_representation.html", title="Vector TSNE representation")
    #
    # pd.set_option('display.max_columns', None)
    # # pd.set_option('display.max_rows', None)
    # p = figure(title='TSNE of Newcastle Venue Vectors', plot_width=1000, plot_height=1000)
    #
    # p.circle("x_values", "y_values", size=8, source=source, legend='col_tag', color="color",
    #          fill_alpha=0.8)
    #
    # labels = LabelSet(x="x_values", y="y_values", text="tags", y_offset=5,
    #                   text_font_size="10px", text_color="black",
    #                   source=source, text_align='center')
    # p.add_layout(labels)
    #
    # show(p)
