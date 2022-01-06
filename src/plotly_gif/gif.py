import os
import sys
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta

from PIL import Image

from . import logging


def get_exec_path():
    try:
        file = os.path.abspath(sys.modules['__main__'].__file__)
    except Exception:
        file = sys.executable
    return os.path.dirname(file)


def format_timedelta(time_: timedelta) -> str:
    total_sec = int(time_.total_seconds())
    sec = total_sec % 60
    min = (total_sec-sec)/60
    return f"{min} min; {sec} sec"


class GIF:
    """

    mode:
        "buffer": no images save
        "png": saves intermediate images to a folder

    """

    def __init__(self,
                 mode: str = "buffer",
                 dir_: str = get_exec_path(),
                 image_path: str = None,
                 gif_path: str = None,
                 verbose: bool = False
                 ):
        self._mode = None
        self.mode = mode

        self.dir_ = Path(dir_)

        if image_path:
            self.image_path = Path(image_path)
        else:
            self.image_path = self.dir_ / "gif_imgs"

        self._image_folder_present = self.image_path.exists()

        if gif_path:
            self.gif_path = Path(gif_path)
        else:
            self.gif_path = self.dir_

        self.verbose = verbose
        self._start_img_create = None

        self.imgs = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        options = ("buffer", "png")
        if mode in options:
            self._mode = mode
        else:
            raise ValueError(f"Acceptable modes: {options}")

    def _create_folder(self):
        """ Create new folder. """
        _folder_name = "temp_gif"
        os.makedirs(_folder_name)
        self.dir_ = os.getcwd() + "\\" + _folder_name
        os.chdir(self.dir_)

        if self.verbose:
            logging.info(f"Folder for images created: {self.dir_}")

    def create_image(self, fig, **kwargs):
        if self._start_img_create is None:
            self._start_img_create = datetime.now()

        if self.mode == "buffer":
            buffer = BytesIO()
            fig.write_image(buffer, format="png", **kwargs)
            buffer.seek(0)
            img = Image.open(buffer)

            if self.imgs is None:
                self.imgs = [img]
            else:
                self.imgs.append(img)
        if self.mode == "png":
            if not self._image_folder_present:
                self._create_folder()
            pass

        if self.verbose:
            logging.info(f"Image {len(self.imgs)} captured. (elapsed time: "
                         f"{format_timedelta(datetime.now()-self._start_img_create)})")

    def create_gif(self, duration=100, unit="ms", **kwargs):
        if unit in ("s", "seconds"):
            duration *= 1000
        elif unit in ("ms", "milliseconds"):
            pass
        else:
            raise ValueError("Acceptable units are: 's', 'seconds', 'ms', 'milliseconds' ")

        _kwargs = {
            "fp": self.gif_path / "fig.gif",
            "append_images": self.imgs[1:],
            "save_all": True,
            "optimize": True,
            "between": "startend",
            "loop": False
        }
        _kwargs = {**_kwargs, **kwargs}

        save_time = datetime.now()
        self.imgs[0].save(**_kwargs)

        if self.verbose:
            logging.info(f"gif created: {self.gif_path} (time to generate gif:"
                         f" {format_timedelta(datetime.now() - save_time)})")


# def png_to_gif(image_arry):
#     """
#     Converts a series of pngs into a gif.
#     https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
#     """
#     image_path = self.dir_ + "//" + "view_*.png"
#     gif_path = self.dir_ + "//" + "fig.gif"
#
#     img, *imgs = [Image.open(f) for f in sorted(glob.glob(image_path))]
#     if self.crop is not None:
#         for i, img_ in enumerate(imgs):
#             imgs[i] = img_.crop(self.crop)
#
#     img.save(fp=gif_path, format='GIF', append_images=imgs, save_all=True,
#              duration=self.duration, loop=0)
#
#     if self.op_printing:
#         print(f"gif created. {gif_path}")
