from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from random import randrange
import requests
from bs4 import BeautifulSoup

f = figure(width=900)

def get_btc_price():
    r=requests.get("https://coinmarketcap.com", headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, "html.parser")
    td = soup.find_all('td', class_='cmc-table__cell--sort-by__price')
    a = td[0].find('a', class_='cmc-link')      # a = '<a href="" class_='cmc-link'>$9,999</a>'
    price = float(a.text[1:].replace(',', ''))  # strip leading $ and remove comma
    print(price)
    return price

def update():
    # create pairs of cordinates for random point
    new_point = dict(x=[source.data['x'][-1]+1], y=[get_btc_price()])
    # stream is new method, rollover specifies max number of points to keep
    source.stream(new_point, rollover=100)
    #print(source.data)

# create empty col data source
source = ColumnDataSource(dict(x=[1], y=[get_btc_price()]))

f.circle(x='x', y='y', color='navy', line_color='red', source=source)
f.line(x='x', y='y', source=source)


# every second we'll generate a pair of coordinates
curdoc().add_root(f)
curdoc().add_periodic_callback(update, 240000)  # every 4 minutes
