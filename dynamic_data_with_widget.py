from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, RadioButtonGroup
from bokeh.plotting import figure
from bokeh.layouts import layout
from random import randrange
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians

def get_coin_price(coin="monero"):
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, "html.parser")
    span = soup.find('span', class_='cmc-details-panel-price__price')
    price = float(span.text[1:].replace(',', ''))   # strip leading dollar sign, remove commas
    print(f"current {coin} price: ${price}")
    return price

def update():
    nameofcoin = options[radio_buttons.active]
    new_point = dict(x=[datetime.now()], y=[get_coin_price(nameofcoin)])
    source.stream(new_point, rollover=100)
    #print(source.data)

def update_intermediate(attr, old, new):
    update()


# make sure X axis can handle datetimes
f = figure(title="Cryptocurrency Prices", x_axis_type='datetime', y_axis_type='linear', plot_width=900)
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

# create radio buttons
#options = [("bitcoin","BTC"),("ethereum", "ETH"),("monero","XMR")]
options = ["bitcoin","ethereum","monero"]
radio_buttons = RadioButtonGroup(labels=options)
radio_buttons.active = 0 # default is bitcoin
radio_buttons.on_change("active", update_intermediate)

l = layout([[radio_buttons]])

# every second we'll generate a pair of coordinates
curdoc().add_root(f)
curdoc().add_root(l)
curdoc().add_periodic_callback(update, 30000)  # every 1 minutes

