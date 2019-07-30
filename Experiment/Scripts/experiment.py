from psychopy import visual, core, event, data, monitors, gui
import random
import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import itertools

def draw():
    introTxt.draw()
    pressKey.draw()
    win.flip()
    event.waitKeys()

def getOriginal(frame_number, path):
    frame = round(frame_number*10)
    if len(str(frame)) == 1:
        image_path = path.split('mask.mp4',2)[0]+'original/animator_0000{}.png'.format(frame)
    elif len(str(frame)) == 2:
        image_path = path.split('mask.mp4',2)[0]+'original/animator_000{}.png'.format(frame)

    return image_path

def getPhosphene(frame_number, path):
    cap = cv2.VideoCapture(path)
    frame = round(frame_number*10)
    cap.set(1,frame)
    ret, image = cap.read()
    im = Image.fromarray(image)
    im.save("temp.png")
    return "temp.png"

original = ['./data/notebook/original.mp4', './data/mouse/original.mp4', './data/pillows/original.mp4',
              './data/fruits/original.mp4', './data/laptop_stock/original.mp4', './data/chair/original.mp4'
              , './data/sofa/original.mp4', './data/mug_stock/original.mp4', './data/pillows_stock/original.mp4'
              , './data/flowers/original.mp4', './data/table/original.mp4', './data/nightstand/original.mp4',
              './data/lamp/original.mp4', './data/keyboard_stock/original.mp4', './data/laptop/original.mp4']

condition0 = ['./data/notebook/phosphene.mp4', './data/mouse/phosphene.mp4', './data/pillows/phosphene.mp4',
              './data/fruits/phosphene.mp4', './data/laptop_stock/phosphene.mp4', './data/chair/phosphene.mp4'
              , './data/sofa/phosphene.mp4', './data/mug_stock/phosphene.mp4', './data/pillows_stock/phosphene.mp4'
              , './data/flowers/phosphene.mp4', './data/table/phosphene.mp4', './data/nightstand/phosphene.mp4',
              './data/lamp/phosphene.mp4', './data/keyboard_stock/phosphene.mp4', './data/laptop/phosphene.mp4']

condition1 = ['./data/notebook/phosphene_ss.mp4', './data/mouse/phosphene_ss.mp4', './data/pillows/phosphene_ss.mp4',
              './data/fruits/phosphene_ss.mp4', './data/laptop_stock/phosphene_ss.mp4', './data/chair/phosphene_ss.mp4'
              , './data/sofa/phosphene_ss.mp4', './data/mug_stock/phosphene_ss.mp4', './data/pillows_stock/phosphene_ss.mp4'
              , './data/flowers/phosphene_ss.mp4', './data/table/phosphene_ss.mp4', './data/nightstand/phosphene_ss.mp4',
              './data/lamp/phosphene_ss.mp4', './data/keyboard_stock/phosphene_ss.mp4', './data/laptop/phosphene_ss.mp4']
condition0_practice = ['./data/lamp_stock/phosphene.mp4', './data/mug/phosphene.mp4', './data/keyboard/phosphene.mp4']
condition1_practice = ['./data/lamp_stock/phosphene_ss.mp4', './data/mug/phosphene_ss.mp4',
                       './data/keyboard/phosphene_ss.mp4']
target_practice = ['lamp', 'mug', 'keyboard']
target = ['notebook', 'mouse', 'pillows', 'fruits', 'laptop', 'chair', 'sofa', 'mug', 'pillows', 'flowers', 'table',
          'nightstand', 'lamp', 'keyboard', 'laptop']
masks = ['./data/notebook/mask.mp4', './data/mouse/mask.mp4', './data/pillows/mask.mp4',
              './data/fruits/mask.mp4', './data/laptop_stock/mask.mp4', './data/chair/mask.mp4'
              , './data/sofa/mask.mp4', './data/mug_stock/mask.mp4', './data/pillows_stock/mask.mp4'
              , './data/flowers/mask.mp4', './data/table/mask.mp4', './data/nightstand/mask.mp4',
              './data/lamp/mask.mp4', './data/keyboard_stock/mask.mp4', './data/laptop/mask.mp4']
masks_practice = ['./data/lamp_stock/mask.mp4', './data/mug/mask.mp4', './data/keyboard/mask.mp4']
k = random.randint(0, 1)
#k = 0
if k == 0:
    stimList = condition0
    practiceList = condition0_practice

elif k == 1:
    stimList = condition1
    practiceList = condition1_practice
print(k)

cur_dir = os.path.dirname(os.path.realpath(__file__))
win = visual.Window((1366, 768), color="black", units="pix")
info = gui.Dlg()
info.addField('Subject:')
info.addField('Age:')
clock = core.Clock()    
mouse = event.Mouse(visible=True,win=win)

introTxt = visual.TextStim(win, text="Welcome!", color='White', height=35, alignHoriz="center")
pressKey = visual.TextStim(win, text="Press any key to continue..", color='White', pos=(0.0, -200))
beginPractice = "Press any key to start the practice trials."
beginExperiment = visual.TextStim(win, text="This is the end of the practice trials. In the next trials the original videos will not be revealed.\n"
                                            "Press any key to start the experiment.", color='White', height=35, alignHoriz="center")
instructions1 = "You will see 15 short videos of 10 seconds each. \nBefore each video, a word will appear on the screen.\nThe word represents a common household item."
instructions2 = "Your task is to search for the object in the video and click on it as fast as possible.\nKeep in mind, you only have 10 seconds for this!"
instructions3 = "After the experiment begins, please keep your hand on the mouse at all times and try to keep the same distance from the screen."
instructions4 = "You will get a chance to practice on 3 videos.\nIf you have any questions, please ask them now."
endTxt = visual.TextStim(win, text="Thanks for participating!", color='White', units="pix", height=35)

confidenceTxt = visual.TextStim(win, text="How sure are you of your choice?", color='White', pos=(0.0,10))
confidenceSlider = visual.RatingScale(win, low=0, high=100, textSize=0.7, labels=('not sure at all', 'neutral','very'),
                                      scale=None, pos=(0.0, -30))
opinionTxt = visual.TextStim(win, text="Overall, how do you think the ", color='White', pos=(0.0,10))
opinionSlider = visual.RatingScale(win, low=0, high=100, textSize=0.7, labels=('not sure at all', 'neutral','very'),
                                      scale=None, pos=(0.0, -766))
targetTxt = visual.TextStim(win, color='White', units="pix", height=35)


ok_data = info.show()
if info.OK:
    file = data.ExperimentHandler(name="Phosphene Experiment", dataFileName="subject_{}".format(ok_data[0]))


file.addData("Condition", k)
file.nextEntry()

while introTxt.status != visual.FINISHED:
    draw()
    introTxt.setText(instructions1)
    draw()
    introTxt.setText(instructions2)
    draw()
    introTxt.setText(instructions3)
    draw()
    introTxt.setText(instructions4)
    draw()
    introTxt.setText(beginPractice)
    introTxt.draw()
    win.flip()
    event.waitKeys()
    introTxt.status = -1


event.clearEvents()
win.flip()

##########################################################################################
# Practice trials

i = 0
for stim in practiceList:
    trial = visual.MovieStim3(win, stim,
                        flipVert=False, flipHoriz=False, loop=False, noAudio=True, size=(160,112))
    mask = visual.MovieStim3(win, masks_practice[i],
                        flipVert=False, flipHoriz=False, loop=False, noAudio=True, size=(160,112), units="pix", opacity=0)

    frame1 = 9.9
    targetTxt.setText("{}".format(target_practice[i]))
    targetTxt.draw()
    win.flip()
    event.waitKeys()
    core.wait(1.0)
    mouse.clickReset()
    while trial.status != visual.FINISHED:
        trial.draw()
        mask.draw()
        win.flip()

        if mouse.isPressedIn(trial):
            mousePos = tuple(mouse.getPos())
            rt = mouse.getPressed(getTime=True)[1][0]
            frame1 = trial.getCurrentFrameTime()
            frame2 = mask.getCurrentFrameTime()
            #print("Frame: ", frame1*10)
            trial.status = -1
            core.wait(1.0)

    while confidenceSlider.noResponse:
        confidenceTxt.draw()
        confidenceSlider.draw()
        win.flip()
    file.addData("Confidence: ", confidenceSlider.getRating())
    confidenceSlider.reset()

    displayFrame_original = visual.ImageStim(win, image=getOriginal(frame1, masks_practice[i]), colorSpace='rgb', units='pix', pos=(-608/2,0))
    displayFrame_phosphene = visual.ImageStim(win, image=getPhosphene(frame1, practiceList[i]), colorSpace='rgb', units='pix', pos=(160, 0))
    displayFrame_original.draw()
    displayFrame_phosphene.draw()
    win.flip()
    event.waitKeys()
    i += 1
    win.flip()
    core.wait(2.0)

core.wait(3.0)


#######################################################################################################
# Experiment

beginExperiment.draw()
win.flip()
event.waitKeys()
i = 0
for stim in stimList:

    trial = visual.MovieStim3(win, stim,
                        flipVert=False, flipHoriz=False, loop=False, noAudio=True, size=(160,112), units="pix")
    mask = visual.MovieStim3(win, masks[i],
                        flipVert=False, flipHoriz=False, loop=False, noAudio=True, size=(160,112), units="pix", opacity=0)



    targetTxt.setText("{}".format(target[i]))
    targetTxt.draw()
    win.flip()
    event.waitKeys()
    core.wait(1.0)

    mouse.clickReset()

    while trial.status != visual.FINISHED:
        trial.draw()
        mask.draw()
        win.flip()

        if mouse.isPressedIn(trial):
            mousePos = tuple(mouse.getPos())
            rt = mouse.getPressed(getTime=True)[1][0]
            frame1 = trial.getCurrentFrameTime()
            frame2 = mask.getCurrentFrameTime()
            file.addData('Pos:', mousePos)
            file.addData('RT:', rt)
            trial.status = -1

            core.wait(1.0)

    while confidenceSlider.noResponse:
        confidenceTxt.draw()
        confidenceSlider.draw()
        win.flip()
    file.addData("Confidence: ", confidenceSlider.getRating())
    confidenceSlider.reset()

    i += 1
    win.flip()
    core.wait(2.0)
    file.nextEntry()


endTxt.draw()
win.flip()
core.wait(3.0)

win.close()
core.quit()
