import numpy as np
import plotly.graph_objs as go
from plotly_gif import GIF, two_d_time_series


# create_gif some data
n = 100
x = np.linspace(0, n-1, n)
y = np.sin(x) + np.random.rand(n)

# create and format plot just the way you like!
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
fig.update_layout(layout)
fig.update_xaxes(xaxis)
fig.update_yaxes(yaxis)

# create gif class to store data
gif = GIF(verbose=True)

# send it to built-in function that will generate gif time_series.
two_d_time_series(gif, fig)
