from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure
from random import randrange
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians

def get_xmr_price():
    r=requests.get("https://coinmarketcap.com/currencies/monero/", headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, "html.parser")
    span = soup.find('span', class_='cmc-details-panel-price__price')
    price = float(span.text[1:])
    print(f'current price: ${price}')
    return price

def update():
    new_point = dict(x=[datetime.now()], y=[get_xmr_price()])
    source.stream(new_point, rollover=100)
    #print(source.data)


# make sure X axis can handle datetimes
f = figure(x_axis_type='datetime', y_axis_type='linear', plot_width=900)
f.xaxis.formatter = DatetimeTickFormatter(
    minutes = ["%Y-%M-%d %H:%M"],
    hours   = ["%Y-%M-%d %H:%M"],
    days    = ["%Y-%M-%d %H:%M"],
    months  = ["%Y-%M-%d %H:%M"],
    years   = ["%Y-%M-%d %H:%M"]
)
f.xaxis.major_label_orientation = radians(60)

# create empty col data source
source = ColumnDataSource(dict(x=[], y=[]))

f.circle(x='x', y='y', color='navy', line_color='red', source=source)
f.line(x='x', y='y', source=source)

# every second we'll generate a pair of coordinates
curdoc().add_root(f)
curdoc().add_periodic_callback(update, 180000)  # every 3 minutes
