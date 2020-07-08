from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.annotations import LabelSet
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import layout

# create columndatasource
source = ColumnDataSource(dict(
    average_grades=[7, 8, 10],
    exam_grades=[6, 9, 8],
    student_names=["Joe", "Fred", "Sally"]
))
osource = ColumnDataSource(dict(average_grades=[7, 8, 10], exam_grades=[6, 9, 8], student_names=["Joe", "Fred", "Sally"]))

f = figure(x_range = Range1d(start=0, end=12), y_range = Range1d(start=0, end=12))

labels = LabelSet(x="average_grades", y="exam_grades", text="student_names", x_offset=-30, y_offset=5, source=source)
f.add_layout(labels)

f.circle(x="average_grades", y="exam_grades", source=source, size=8)

def update_labels(attr, old, new):
    labels.text = select.value

# create filtering function
def filter_grades(attr, old, new):
    # for each key,value in original iterate and build new source.data if average_grade > slider value
    source.data = {
        key:[value for i, value in enumerate(osource.data[key]) if osource.data["exam_grades"][i] >= slider.value] for key in osource.data}
    #print(slider.value)


# create select widget
options = [("average_grades", "Average Grades"), ("exam_grades", "Exam Grades"), ("student_names", "Student Names")]
select = Select(title="Attribute", options=options)
select.on_change("value", update_labels)

# create slider widget
slider = Slider(start=min(osource.data["exam_grades"])-1, end=max(osource.data["exam_grades"])+1, value=7, step=0.5, title="Exam Grade")
slider.on_change("value", filter_grades)

l = layout([[select],[slider]])

curdoc().add_root(f)
curdoc().add_root(l)

