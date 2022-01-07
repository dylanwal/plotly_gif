import copy

import plotly.graph_objs as go

from . import GIF


def two_d_time_series(
        gif_: GIF,
        fig: go.Figure,
        frames: int = 60,
        auto_create: bool = True,
        gif_kwargs: dict = None,
):
    """

    Parameters
    ----------
    gif_: GIF
        GIF object to store data in
    fig: go.Figure
        Plotly Figure
        Add all the data and formatting before passing it in.
    frames: int
        Number of frames you want in the gif
        default = 60
    auto_create: bool
        automatically create gif
        default = True
        If false you can just generate it yourself with gif_.create_gif() and pass any kwargs you like
    gif_kwargs: dict
        kwargs passed to create_gif

    """
    # Copy data, so we don't overwrite anything
    fig = copy.copy(fig)
    data = {}
    for i, trace in enumerate(fig.data):
        if isinstance(trace, go.Scatter):
            data[i] = {
                "trace": copy.copy(trace),
                "len": len(trace.x),
                "step": int(len(trace.x) / frames)
            }

    # Loop though frame by frame to create gif
    for frame in range(frames):
        # loop through each trace and change length
        for index, data_ in data.items():
            fig.data[index].x = data_["trace"].x[0: frame*data_["step"]]
            fig.data[index].y = data_["trace"].y[0: frame * data_["step"]]

        gif_.create_image(fig)

    if auto_create:
        gif_.create_gif(**gif_kwargs if gif_kwargs is not None else {})
