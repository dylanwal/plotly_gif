import numpy as np
import plotly.graph_objs as go

from . import GIF


def three_d_scatter_rotate(
        gif_: GIF,
        fig: go.Figure,
        frames: int = 60,
        viewer_position: tuple = (-1.25, 2, 0.5),
        rotation: tuple = (0, 2*np.pi),
        auto_create: bool = True,
        gif_kwargs: dict = None
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
    viewer_position: tuple[x, y, z]
        initial viewer/camera position
    rotation: tuple[start, end]
        range of rotation (in radians)
    auto_create: bool
        automatically create gif
        default = True
        If false you can just generate it yourself with gif_.create_gif() and pass any kwargs you like
    gif_kwargs: dict
        kwargs passed to create_gif
    """

    angles = np.arange(*rotation, np.abs(rotation[1]-rotation[0])/frames)

    for i, t in enumerate(angles):
        x, y, z = rotate_z(*viewer_position, -t)
        fig.update_layout(
            scene_camera=dict(eye=dict(x=x, y=y, z=z))
            # plot_bgcolor="rgba(0, 0, 0, 0)",
            # paper_bgcolor="rgba(0, 0, 0, 0)"
        )
        gif_.create_image(fig)

    if auto_create:
        gif_.create_gif(**gif_kwargs if gif_kwargs is not None else {})


def rotate_z(x: float, y: float, z: float, theta: float):
    w = x + 1j * y
    return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z



def gif_df(gif_: GIF, df: pd.DataFrame, x_col: str, y_col: str, z_col:str, t_col: str):
    t_values = np.sort(df[t_col].unique())
    x = df["light_height"].unique()
    y = df["light_width"].unique()
    x = np.sort(x)
    y = np.sort(y)
    for t in t_values:
        fig = go.Figure()
        df_local = df[df[t_col] == t]
        z = np.empty((len(x), len(y)))
        for i in range(len(x)):
            for ii in range(len(x)):
                z[ii, i] = df_local[z_col].loc[(df_local[x_col] == x[i]) & (df_local[y_col] == y[ii])]

        fig.add_trace(go.Surface(x=x, y=y, z=z))
        gif_.create_image(fig)
        
