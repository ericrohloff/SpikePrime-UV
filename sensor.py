# Get data from the DOM for the sensor and put it on the graph
from pyscript import document, window, when


@when("click", "#to_python")
def on_python(event):
