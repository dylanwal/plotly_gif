from functools import wraps
import logging

from plotly_gif.gif import GIF
from plotly_gif.two_d_plots import two_d_time_series
from plotly_gif.three_d_plots import three_d_scatter_rotate

__all__ = ["GIF", "capture", "two_d_time_series", "three_d_scatter_rotate"]

logging.basicConfig(level=logging.INFO, format='  %(message)s')


def capture(gif_: GIF):
    """ Capture
    Captures images as they are created.

    Parameters
    ----------
    gif_: GIF
        gif object that stores images

    """
    def capture_decorator(func):
        @wraps(func)
        def _capture(*args, **kwargs):
            fig = func(*args, **kwargs)
            gif_.create_image(fig)
            return fig

        return _capture

    return capture_decorator
