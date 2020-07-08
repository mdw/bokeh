from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from random import randrange

f = figure(x_range=(0,11), y_range=(0,11))

# create empty col data source
source = ColumnDataSource(dict(x=[], y=[]))

f.circle(x='x', y='y', color='navy', line_color='red', source=source)
f.line(x='x', y='y', source=source)

def update():
    # create pairs of cordinates for random point
    new_point = dict(x=[randrange(1,10)], y=[randrange(1,10)])
    # stream is new method, rollover specifies max number of points to keep
    source.stream(new_point, rollover=12)
    #print(source.data)

# every second we'll generate a pair of coordinates
curdoc().add_root(f)
curdoc().add_periodic_callback(update, 1000)
