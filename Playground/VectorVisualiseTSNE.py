import random
from sklearn.manifold import TSNE
import sqlite3
import pickle
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure, output_file, show
import numpy as np

db_obj = sqlite3.connect(
    '/Users/benlongcroft/Documents/Nitely Project/NewDB/ExperimentalOrficDB.db')
cursor_obj = db_obj.cursor()
pickle_off = open("club_vectors_31-01-2021.txt", "rb")
vectors = pickle.load(pickle_off)
vectors = [x[0] for x in vectors]

cursor_obj.execute('''SELECT name FROM venue_info  WHERE description != 'DO NOT USE';''')
names = [x[0] for x in cursor_obj.fetchall()]

tsne = TSNE(perplexity=30, n_components=2, init='pca', early_exaggeration=7, learning_rate=100, n_iter=3000, n_iter_without_progress=1000, random_state=23)

new_values = tsne.fit_transform(vectors)

x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

r = {'x_values':x, 'y_values':y, 'tags':names}
source = ColumnDataSource(pd.DataFrame(r, columns = ['x_values', 'y_values', 'tags']))

output_file("TSNE_representation.html", title="Vector TSNE representation")


print(source)
p = figure(title='TSNE of Newcastle Venue Vectors', plot_width=1000, plot_height=1000)

p.circle("x_values", "y_values", size=8, source=source, line_color="black", fill_alpha=0.8)

labels = LabelSet(x="x_values", y="y_values", text="tags", y_offset=5,
                  text_font_size="10px", text_color="#555555",
                  source=source, text_align='center')
p.add_layout(labels)


show(p)