from typing import List
import os
from PIL import Image
from PIL.Image import Image as ImageClass
from collections import OrderedDict

from frontend import AnnotatorFrontend

BoundingBox = List[int]

class AnnotatorBackend:

    def __init__(self,
                 img_dir: str,
                 ann_dir: str,
                 classes: List[str],
                 keys: List[str],
                 labels: List[int]) -> None:
        self.img_dir = img_dir.rstrip('/') + '/'
        self.ann_dir = ann_dir.rstrip('/') + '/'
        self.classes = classes 
        self.keys = keys
        self.labels = labels
        self.frontend = AnnotatorFrontend()
        self.current_index = -1
        self.current_img_filename = ''
        self.unlabeled_bboxes: List[BoundingBox] = []
        self.labeled_bboxes: List[BoundingBox] = []

    def ann_loop(self) -> int:
        annotation = ''
        key2lbl = {key : lbl for key, lbl in zip(self.keys, self.labels)}
        while annotation not in key2lbl:
            annotation = input()
        return key2lbl[annotation]

    def save(self) -> None:
        current_ann_filename = self.current_img_file[:-3] + 'txt'
        with open(self.ann_dir + current_ann_filename, 'w') as file:
            for bbox in self.labeled_bboxes:
                file.write(' '.join([str(x) for x in bbox]))
                file.write('\n')      
        self.labeled_bboxes = []
    
    def main_loop(self) -> None:
        if self.unlabeled_bboxes:
            current_bbox = self.unlabeled_bboxes.pop()
            self.frontend.display_bbox(current_bbox)
            current_bbox.append(self.ann_loop())
            self.labeled_bboxes.append(current_bbox)
        elif self.labeled_bboxes:
            self.save()
        else:
            try:
                self.load_next()
            except IndexError as e:
                return None
            if self.unlabeled_bboxes:
                self.frontend.display_image(self.get_image())
                self.frontend.display_legend(self.classes, self.keys)
            else:
                self.labeled_bboxes = []
        self.main_loop()

    def load_next(self) -> None:
        self.current_index += 1
        self.current_img_file = os.listdir(self.img_dir)[self.current_index]
        with open(self.ann_dir + self.current_img_file[:-3] + 'txt') as file:
            for line in file.readlines():
                bbox = [int(x) for x in line.split()]
                if len(bbox) == 8:
                    self.unlabeled_bboxes.append(bbox)
                elif len(bbox) == 9:
                    self.labeled_bboxes.append(bbox)
                else:
                    raise ValueError(f"Parsing failed: {bbox}")

    def get_image(self) -> ImageClass:
        return Image.open(self.img_dir + self.current_img_file)
