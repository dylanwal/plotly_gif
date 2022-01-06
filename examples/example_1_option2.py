import numpy as np
import plotly.graph_objs as go
from plotly_gif import GIF


# create_gif some data
n = 100
x = np.linspace(0, n-1, n)
y = np.sin(x) + np.random.rand(n)

# Create gif class to store data
gif = GIF(verbose=True)


def plot_(x_, y_):
    # Function that generates  plotly figures
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_, y=y_, mode="lines"))

    gif.create_image(fig)  # tells gif to save each figure
    return fig


frames = 60
for i in range(1, n, int(n/frames)):
    # Changes the range of the data each step to make it look like a time series
    plot_(x[0: i], y[0: i])

# Function that generates new plotly figures
gif.create_gif()
