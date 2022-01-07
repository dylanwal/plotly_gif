import numpy as np
import plotly.graph_objs as go
from plotly_gif import GIF, three_d_scatter_rotate

# generate data
t = np.linspace(0, 10, 50)
x, y, z = np.cos(t), np.sin(t), t

# create figure
fig = go.Figure(go.Scatter3d(x=x, y=y, z=z, mode='markers'))

# view figure in html
#fig.write_html('temp.html', auto_open=True)

# create gif
gif = GIF(mode="png")
three_d_scatter_rotate(gif, fig)
