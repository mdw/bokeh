from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.annotations import LabelSet
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
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
    labels.text = select.value

# create select widget
options = [("average_grades", "Average Grades"), ("exam_grades", "Exam Grades"), ("student_names", "Student Names")]
select = Select(title="Attribute", options=options)
select.on_change("value", update_labels)

l = layout([[select]])
curdoc().add_root(f)
curdoc().add_root(l)

