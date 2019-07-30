import imageio
import os
import cv2
from PIL import Image

mask = os.path.abspath("/home/coco/thesisExperiment/data/table/mask/")
original = os.path.abspath("/home/coco/thesisExperiment/data/table/original/")

def video_mask(path_mask):
    out = []
    for frame in sorted(os.listdir(path_mask)):
        print(frame)
        path = os.path.join(path_mask, frame)
        image = Image.open(path)
        out.append(image)

    imageio.mimwrite("/home/coco/thesisExperiment/data/table/mask.mp4", out , fps = 10)

def video_original(path_original):
    out = []
    for frame in sorted(os.listdir(path_original)):
        print(frame)
        path = os.path.join(path_original, frame)
        image = Image.open(path)
        out.append(image)

    imageio.mimwrite("/home/coco/thesisExperiment/data/table/original.mp4", out , fps = 10)

video_mask(mask)
video_original(original)
