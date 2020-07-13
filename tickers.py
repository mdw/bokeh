import requests
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, RadioButtonGroup
from bokeh.models import HoverTool, PanTool, ResetTool, SaveTool
from bokeh.plotting import figure
from bokeh.layouts import layout
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians
from random import randrange


# store a dict of points on a graph
source = ColumnDataSource(data=dict(x=[], y=[], coin=[]))
options = ["bitcoin","ethereum","monero"]


def get_coin_price(ticker="bitcoin"):
    url = f"https://coinmarketcap.com/currencies/{ticker}/"
    r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, "html.parser")
    span = soup.find('span', class_='cmc-details-panel-price__price')
    price = float(span.text[1:].replace(',', ''))   # strip leading dollar sign, remove commas
    #print(f"current {ticker} price: ${price}")
    return price

def update():
    # change data to add a new graph point 
    new_point = dict(
            x=[datetime.now()], 
            y=[get_coin_price(options[radio_buttons.active])], 
            coin=[radio_buttons.active])
    source.stream(new_point, rollover=72)
    #print(source.data)


def update_ticker(attr, old, new):
    # if crypto choice changed, clear plot
    source.data = dict(x=[], y=[], coin=[])
    update()


f = figure(x_axis_type='datetime', y_axis_type='linear')
f.plot_width = 1024
f.title.text = "Cryptocurrency Price Plot"
f.title.text_color = "navy"
f.title.text_font_size = "25px"

# make sure X axis can handle datetimes
f.xaxis.formatter = DatetimeTickFormatter(
    minutes = ["%Y-%M-%d, %H:%M"],
    hours   = ["%Y-%M-%d, %H:%M"],
    days    = ["%Y-%M-%d, %H:%M"],
    months  = ["%Y-%M-%d, %H:%M"],
    years   = ["%Y-%M-%d, %H:%M"]
)
f.xaxis.major_label_orientation = radians(60)

f.background_fill_color = "navy"
f.background_fill_alpha = 0.1

f.circle(x='x', y='y', color='navy', line_color='red', source=source)
f.line(x='x', y='y', source=source)

radio_buttons = RadioButtonGroup(labels=options)
radio_buttons.active = 0   # default bitcoin
radio_buttons.on_change("active", update_ticker)

f.tools = [PanTool(), ResetTool(), SaveTool()]
f.toolbar.logo = None
ht = HoverTool(tooltips=[("Price", "@y{($ 0.00)}")])
f.add_tools(ht)


l = layout([[radio_buttons]])
curdoc().add_root(f)
curdoc().add_root(l)

# find alt source that updates more frequently
curdoc().add_periodic_callback(update, 210000)  # every 3.5 minutes

