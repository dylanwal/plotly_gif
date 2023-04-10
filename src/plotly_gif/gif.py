import os
import sys
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta
import glob
import copy
import re
import logging

from PIL import Image


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


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """ sorts in human order """
    return [atoi(c) for c in re.split(r'(\d+)', text)][1]


class GIF:
    """

    mode:
        "buffer": no images save
        "png": saves intermediate images to a folder
    dir_: str
        directory to for data storage
    image_path: str
        where .png will be saved
        default: gif_imgs in working directory

    """

    def __init__(self,
                 mode: str = "buffer",
                 dir_: str = get_exec_path(),
                 image_path: str = None,
                 gif_name: str = None,
                 gif_path: str = None,
                 verbose: bool = True
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

        if gif_name is not None:
            if not gif_name.endswith(".gif"):
                gif_name = gif_name + ".gif"
        self.gif_name = gif_name

        self.verbose = verbose
        self._start_img_create = None

        self.imgs = None
        self.num_images = 0

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
        os.makedirs(self.image_path)

        if self.verbose:
            logging.info(f"Folder created for images: {self.dir_}")

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
                self._image_folder_present = True
                self._create_folder()
            png_path = self.image_path / f"img_{self.num_images}.png"
            fig.write_image(png_path)

        self.num_images += 1

        if self.verbose:
            logging.info(f"Image {self.num_images} captured. (elapsed time: "
                         f"{format_timedelta(datetime.now()-self._start_img_create)})")

    def create_gif(self, length: int = 3000, crop: tuple = None, gif_path: str =None, **kwargs):
        """

        Parameters
        ----------
        length: int
            length of gif in milliseconds
        crop: tuple[left, top, right, bottom]
            crop gif
        gif_path: str
            anther way to choose the gif path and name.
            ! path must end with '.gif' !
        kwargs:
            See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif

        """
        if gif_path is None:
            gif_path = self.gif_path / "fig.gif" if self.gif_name is None else self.gif_path / self.gif_name
        else:
            if not gif_path.endswith(".gif"):
                raise ValueError(f"gif path must end with '.gif'. Provide value: {gif_path}")

        _kwargs = {
            "fp": gif_path,
            "save_all": True,
            "optimize": True,
            "between": "startend",
            "loop": False
        }
        _kwargs = {**_kwargs, **kwargs}

        imgs = self.imgs

        if self.imgs is None:  # try to load in pngs if images not in buffer
            imgs = [Image.open(f) for f in sorted(glob.glob(str(self.image_path / "*.png")), key=natural_keys)]

        if crop is not None:
            imgs = copy.copy(imgs)  # prevent editing
            for i, img_ in enumerate(imgs):
                imgs[i] = img_.crop(crop)

        if "duration" not in kwargs:
            _kwargs["duration"] = length/len(imgs)

        save_time = datetime.now()
        imgs[0].save(append_images=imgs[1:], **_kwargs)

        if self.verbose:
            logging.info(f"gif created: {gif_path} (time to generate gif:"
                         f" {format_timedelta(datetime.now() - save_time)})")

