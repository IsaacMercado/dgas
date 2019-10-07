from plotly import graph_objs as go
from plotly import offline

plot = lambda figure: offline.plot(figure, output_type='div', include_plotlyjs=False)