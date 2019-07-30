import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from phophenefilter import to_phosphene
import imageio
from PIL import Image

def original(path, output_path):
    frames = []
    for file in sorted(os.listdir(path)):
        frames.append(Image.open(os.path.join(path,file)))
    imageio.mimwrite(os.path.join(output_path,'original.mp4'), frames , fps = 10)
    return frames
def edgeDetection(path, output_path, p1, p2):
    print(path)
    edges = []
    cap = cv2.VideoCapture(path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            edges.append(cv2.Canny(frame,p1,p2))
        else:
            break
    cap.release()
    imageio.mimwrite(output_path, edges , fps = 10)
    return edges

def phosphene(edges_path, output_path):
    phosphenes = []
    print(edges_path)
    cap = cv2.VideoCapture(edges_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            phosphenes.append(to_phosphene(frame))
        else:
            break
    cap.release()
    imageio.mimwrite(output_path, phosphenes , fps = 10)
    return phosphenes

names = ["chair", "flowers", "fruits", "keyboard", "keyboard_stock", "lamp", "lamp_stock", "laptop",
         "laptop_stock", "mouse", "mug", "mug_stock", "nightstand", "notebook", "pillows", "pillows_stock", "sofa", "table"]

for name in names:
    #basename = os.path.abspath("/home/coco/thesisExperiment/data/{}/".format(name))
    #ss = os.path.abspath("/home/coco/thesisExperiment/data/{}/segmentation.mp4".format(name))

    original_path = os.path.abspath("/home/coco/thesisExperiment/data/{}/original.mp4".format(name))
    #original = original(original_path, basename)

    #edge = edgeDetection(original_path, '/home/coco/thesisExperiment/data/{}/edge.mp4'.format(name), 100, 200)
    edge_path = os.path.abspath('/home/coco/thesisExperiment/data/{}/edge.mp4'.format(name))
    phosphene(edge_path, "/home/coco/thesisExperiment/data/{}/phosphene.mp4".format(name))

    #edge_ss = edgeDetection(ss, '/home/coco/thesisExperiment/data/{}/edge_ss.mp4'.format(name), 20, 50)
    edge_ss_path = os.path.abspath('/home/coco/thesisExperiment/data/{}/edge_ss.mp4'.format(name))
    phosphene(edge_ss_path, "/home/coco/thesisExperiment/data/{}/phosphene_ss.mp4".format(name))


