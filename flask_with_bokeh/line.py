from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

x=[1,2,3,4,5]
y=[2,4,6,8,10]

f = figure()
f.line(x,y)

# components is a tuple, store html pieces
script, div = components(f)

cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0] if len(CDN.css_files) else ""
