from typing import Tuple, OrderedDict, List
import matplotlib.pyplot as plt
from PIL.Image import Image as ImageClass

BoundingBox = List[int]

class AnnotatorFrontend:

    def __init__(self,
        figsize: Tuple[int, int] = (10, 10)) -> None:
        plt.ion()
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.img = None
        self.bbox = None

    def display_image(self, img: ImageClass) -> None:
        if self.img is None:
            self.img = self.ax.imshow(img)
        else:
            self.img.set_data(img)

    def display_legend(self, keys: List[str], classes: List[str]) -> None:
        for key, _class in zip(keys, classes):
            self.ax.scatter(0, 0, alpha=0, label=f"{_class}: {key}")
        self.ax.legend()
        self.bbox = None

    def display_bbox(self, bbox: BoundingBox) -> None:
        if self.bbox is not None:
            self.bbox.remove()
        x1, y1, x2, y2, x3, y3, x4, y4 = bbox
        self.ax.plot([y1, y2, y3, y4, y1], [x1, x2, x3, x4, x1], color='red')