import numpy as np
import plotly.graph_objs as go
from plotly_gif import GIF, two_d_time_series
from plotly_gif.format_ import layout, xaxis, yaxis


# create_gif some data
n = 100
x = np.linspace(0, n-1, n)
y = np.sin(x) + np.random.rand(n)
x2 = x*0.75
y2 = np.cos(x2) + np.random.rand(n)

# create and format plot just the way you like!
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
fig.add_trace(go.Scatter(x=x2, y=y2, mode="lines"))
fig.update_layout(layout)
fig.update_xaxes(xaxis)
fig.update_yaxes(yaxis)

# create gif class to store data
gif = GIF(mode="png", gif_name="exmaple2", verbose=True)

# send it to built-in function that will generate gif time_series.
two_d_time_series(gif, fig, gif_kwargs={"length": 8000})
