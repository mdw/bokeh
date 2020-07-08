from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.annotations import LabelSet
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import layout

# create columndatasource
source = ColumnDataSource(dict(
    average_grades=["B+", "C", "A+"],
    exam_grades=["A", "B-", "A"],
    student_names=["Joe", "Fred", "Sally"]
))

f = figure(x_range=["F","D-","D","D+","C-","C","C+","B-","B","B+","A-","A","A+"], 
        y_range=["F","D-","D","D+","C-","C","C+","B-","B","B+","A-","A","A+"]
)

labels = LabelSet(x="average_grades", y="exam_grades", text="student_names", x_offset=-30, y_offset=5, source=source)
f.add_layout(labels)

f.circle(x="average_grades", y="exam_grades", source=source, size=8)

def update_labels(attr, old, new):
    labels.text = options[radio_button_group.active]

# create select widget
options = ["average_grades", "exam_grades", "student_names"]
radio_button_group = RadioButtonGroup(labels=options)
radio_button_group.on_change("active", update_labels)

l = layout([[radio_button_group]])
curdoc().add_root(f)
curdoc().add_root(l)

