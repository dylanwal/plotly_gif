import copy

import plotly.graph_objs as go

from . import gif


def two_d_time_series(gif_: gif, fig: go.Figure, frames: int = 60, auto_create: bool = True):
    fig = copy.copy(fig)
    data = {}
    for i, trace in enumerate(fig.data):
        if isinstance(trace, go.Scatter):
            data[i] = {
                "trace": copy.copy(trace),
                "len": len(trace.x),
                "step": int(len(trace.x) / frames)
            }

    for frame in range(frames):
        for index, data_ in data.items():
            fig.data[index].x = data_["trace"].x[0: frame*data_["step"]]
            fig.data[index].y = data_["trace"].y[0: frame * data_["step"]]
            gif_.create_image(fig)

    if auto_create:
        gif_.create_gif()
