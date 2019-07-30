import os
import cv2

base = os.path.abspath("/home/coco/thesisExperiment/data/lamp_stock/")
seg = os.path.join(base, "original.mp4")
#frames = [0, 24, 49, 74, 99]
frames = [0]

print(seg)

for frame in frames:
    cap = cv2.VideoCapture(seg)
    cap.set(1,frame)
    ret, image = cap.read()
    cv2.imwrite("lamp.png" , image)
