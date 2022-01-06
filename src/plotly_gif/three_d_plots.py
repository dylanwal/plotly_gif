import copy

import plotly.graph_objs as go

from . import gif

def three_d_scatter_rotate():
    pass


import multiprocessing as mp
from typing import List, Optional, Tuple
import os
import datetime
import glob

from PIL import Image
import plotly.graph_objects as go
import numpy as np


class FigToGif:
    def __init__(self,
                 fig: Optional[go.Figure] = None,
                 name: Optional[str] = "gif_data",
                 dir_: Optional[str] = None,
                 viewer_position: Optional[List[float]] = None,
                 num_frames: Optional[int] = 60,
                 duration: Optional[float] = 60,
                 img_width: Optional[int] = 1000,
                 img_height: Optional[int] = 1000,
                 crop: Optional[Tuple[int, int, int, int]] = None,
                 op_printing: Optional[bool] = True,
                 op_create_folder: Optional[bool] = True,
                 op_parallel: Optional[bool] = False,
                 ):
        """
        Turns plotly 3d figures into gifs
        :param fig: plotly figure
        :param name: name of files
        :param dir_: directory where you want the files to be created
        :param viewer_position: initial viewer/camera position
        :param num_frames: number of frames in gif
        :param duration: time each frame is shown in the gif (milliseconds)
        :param crop: crop gif (left, top, right, bottom)
        :param op_printing: OPTION: print progress to terminal
        :param op_create_folder: OPTION: put png's in folder
        :param op_parallel: Enable parallel or multiprocessing to speed up generation of png's
        """
        self.name = name
        self.fig = fig
        self.dir_ = dir_

        if viewer_position is None:
            self.viewer_position = [-1.25, 2, 0.5]
        else:
            self.viewer_position = viewer_position

        self.num_frames = num_frames
        self.duration = duration
        self.crop = crop
        self.img_width = img_width
        self.img_height = img_height

        self.op_printing = op_printing
        self.op_create_folder = op_create_folder
        self.op_parallel = op_parallel

    def create_gif(self):
        """ Main function at turning plotly fig to gif. """
        if self.fig is None:
            raise ValueError("fig needs to be a plotly figure to used this function.")

        self._create_folder()
        if self.op_parallel:
            self._create_png_series_multi()
        else:
            self._create_png_series()
        self.png_to_gif()

    def _create_folder(self):
        """ Create new folder. """
        if self.dir_ is not None:
            os.chdir(self.dir_)

        if self.op_create_folder:
            _date = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            _folder_name = f"{self.name}_{_date}"
            os.makedirs(_folder_name)
            self.dir_ = os.getcwd() + "\\" + _folder_name
            os.chdir(self.dir_)

            if self.op_printing:
                print(f"Directory {self.dir_} created.")

    def _create_png_series(self):
        """ Creates a series of pngs at different angles for a 3D plotly plot."""
        _angle_step = (2 * np.pi) / self.num_frames
        for i, t in enumerate(np.arange(0, 2 * np.pi, _angle_step)):
            x, y, z = self.rotate_z(*self.viewer_position, -t)
            self.fig.update_layout(
                scene_camera=dict(eye=dict(x=x, y=y, z=z))
                # plot_bgcolor="rgba(0, 0, 0, 0)",
                # paper_bgcolor="rgba(0, 0, 0, 0)"
            )
            self.fig.write_image(f"view_{t}.png")

            if self.op_printing:
                print(f"png {i}/{self.num_frames} created.")

    def _create_png_series_multi(self):
        """ Creates a series of pngs at different angles for a 3D plotly plot."""
        _angle_step = (2 * np.pi) / self.num_frames
        t = np.arange(0, 2 * np.pi, _angle_step)
        i = np.linspace(0, self.num_frames-1, self.num_frames, dtype="int8")
        with mp.Pool(3) as p:
            p.starmap(self._set_png, zip(i, t))

    def _set_png(self, i, t):
        x, y, z = self.rotate_z(*self.viewer_position, -t)
        self.fig.update_layout(
            scene_camera=dict(eye=dict(x=x, y=y, z=z)),
        )
        self.fig.write_image(f"view_{t}.png", height=self.img_height, width=self.img_width)

        if self.op_printing:
            print(f"png {i}/{self.num_frames} created.")

    def png_to_gif(self):
        """
        Converts a series of pngs into a gif.
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        """
        image_path = self.dir_ + "//" + "view_*.png"
        gif_path = self.dir_ + "//" + "fig.gif"

        img, *imgs = [Image.open(f) for f in sorted(glob.glob(image_path))]
        if self.crop is not None:
            for i, img_ in enumerate(imgs):
                imgs[i] = img_.crop(self.crop)

        img.save(fp=gif_path, format='GIF', append_images=imgs, save_all=True,
                 duration=self.duration, loop=0)

        if self.op_printing:
            print(f"gif created. {gif_path}")

    @staticmethod
    def rotate_z(x: float, y: float, z: float, theta: float):
        w = x + 1j * y
        return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z


def testing():
    # create_gif plot
    t = np.linspace(0, 10, 50)
    x, y, z = np.cos(t), np.sin(t), t
    fig = go.Figure(go.Scatter3d(x=x, y=y, z=z, mode='markers'))
    # fig.write_html('temp.html', auto_open=True)

    gif = FigToGif(fig, op_parallel=False, crop=(200, 200, 800, 800))
    gif.create_gif()

    # gif = FigToGif()
    # gif.dir_ = r"C:\Users\nicep\Desktop\Reseach_Post\Case_studies\raytracepy\examples\gif_data_2021_11_04-10_42_33_PM"
    # gif.png_to_gif()


if __name__ == "__main__":
    testing()