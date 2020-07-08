#from bokeh.io import output_file, show
from bokeh.io import curdoc
from bokeh.models.widgets import TextInput, Button, Paragraph
from bokeh.layouts import layout

### either one of these to execute: 
### $ python -m bokeh serve widgets.py
### $ bokeh serve widgets.py

#output_file('simple_bokeh.html')

#create widgets
text_input = TextInput(value="Joe")
button = Button(label="Generate Text")
output = Paragraph()

def update():
    output.text = "Hello " + text_input.value

button.on_click(update)

# 2 rows for layout: button + text input, and output
layout1 = layout([[button, text_input], [output]])
#show(layout1)

curdoc().add_root(layout1)
