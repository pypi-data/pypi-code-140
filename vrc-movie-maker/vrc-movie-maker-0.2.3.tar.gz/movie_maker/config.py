from abc import ABCMeta, abstractmethod
import hashlib
from pathlib import Path
from typing import List
from dataclasses import dataclass


@dataclass
class MovieConfig:
    """
    Movie config.
    :param input_image_dir: image directory path.
    :param output_movie_path: output movie file path.
    :param width: movie width.
    :param image_type: image file type.
    :param frame_rate: frame per second.
    :param speed: 'veryslow', 'slower', 'slow', 'medium', 'fast', 'faster', 'veryfast', 'superfast', 'ultrafast'
    """
    input_image_dir: Path
    output_movie_path: Path
    width: int = 1280
    image_type: str = 'png'
    frame_rate: int = 4
    max_frame_rate: int = 4
    encode_speed = 'medium'

    def __post_init__(self):
        if self.frame_rate > self.max_frame_rate:
            raise ValueError(f'frame_rate should be less than {self.max_frame_rate}')
        if self.width % 2 != 0:
            self.width += 1
        if self.output_movie_path.suffix != '.mp4':
            self.output_movie_path = Path(f"{self.output_movie_path}.mp4")


class BaseConfig(metaclass=ABCMeta):
    """
    This class is used to create a hash of the config object.
    """
    fps = 1

    def __post_init__(self) -> None:
        self.apply_limit()

    @property
    def hash(self) -> str:
        return hashlib.sha3_256(str(self.__dict__).encode()).hexdigest()

    @abstractmethod
    def apply_limit(self) -> None:
        pass


@dataclass
class ImageConfig(BaseConfig):
    """
    This class used to Input Image Config.
    :param image_dir: image directory path.
    :param width: image width.
    :param height: image height.
    :param max_width: max image width.
    :param max_height: max image height.
    """
    image_dir: Path
    width: int = 1280
    height: int = 720
    # limit of image size.
    max_width = 1920
    max_height = 1920

    def apply_limit(self) -> None:
        if self.max_width < self.width: self.width = self.max_width
        if self.max_height < self.height: self.height = self.max_height


@dataclass
class BrowserConfig(BaseConfig):
    """
    This class used to Browser Config.
    locale is set by lang.
    :param url: url.
    :param width: browser width.
    :param height: browser height.
    :param page_height: page height.
    :param scroll: scroll.
    :param traget: select target file name or type.
    :param lang: browser language.
    :param max_width: max browser width.
    :param max_height: max browser height.
    :param max_page_height: max page height.
    :param min_scroll: min scroll.
    :param driver: driver path.
    :param page_load_timeout: page load timeout.
    """
    # user inputs
    url: str = ''
    width: int = 1280
    height: int = 720
    page_height: int = 50000
    scroll: int = 200
    lang: str = 'en-US'
    targets: List[str] = None
    # limits for browser
    min_scroll = 200
    min_page_height = 3000
    max_page_height = 100000
    max_width = 1920
    max_height = 1920
    # driver settings
    driver_path = Path(__file__).parent
    page_load_timeout = 20
    # set in __post_init__
    locale: str = 'en_US'

    def __post_init__(self):
        if self.url != '': self.domain = self.url.split("/")[2]
        self.locale = self.lang.replace('-', '_')
        super().__post_init__()

    def apply_limit(self) -> None:
        if self.max_width < self.width: self.width = self.max_width
        if self.max_height < self.height: self.height = self.max_height
        if self.max_page_height < self.page_height: self.page_height = self.max_page_height
        if self.scroll < self.min_scroll: self.scroll = self.min_scroll
