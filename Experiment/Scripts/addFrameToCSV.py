import os
from PIL import Image
import numpy as np
import pandas as pd
import csv

directory = os.path.abspath("/home/coco/thesisExperiment/experiment_data/")

masks = ['../data/notebook/mask', '../data/mouse/mask', '../data/pillows/mask',
              '../data/fruits/mask', '../data/laptop_stock/mask', '../data/chair/mask'
              , '../data/sofa/mask', '../data/mug_stock/mask', '../data/pillows_stock/mask'
              , '../data/flowers/mask', '../data/table/mask', '../data/nightstand/mask',
              '../data/lamp/mask', '../data/keyboard_stock/mask', '../data/laptop/mask']

writer = csv.writer(open('../data.csv',"w"), delimiter=',',quoting=csv.QUOTE_NONE)
writer.writerow(['subject','condition','RT','score', 'confidence'])
final_df = pd.DataFrame(columns=['Subject','Condition','RT','Score', 'Confidence'])
print("Final dataframe: ", final_df)

for subject in sorted(os.listdir(directory)):

    results = []
    frames = []
    positions_phosphene = []
    positions_mask = []
    scores = []

    path = os.path.join(directory, subject)
    base, _ = os.path.splitext(subject)

    print("Subject: ", base)

    df = pd.read_csv(path)

    condition = df['Condition'][0]
    print("Condition: ", condition)
    df = df.drop(index=0)
    print(df)



    for rt in df['RT:']:
        if np.isnan(rt):
            frames.append(np.nan)
        else:
            frame = round(rt*10)
            frames.append(frame)

    for st in df['Pos:']:
        if pd.isnull(st):
            positions_mask.append(np.nan)
        else:
            x, y = eval(st)
            positions_phosphene.append((x+80, np.abs(y-56)))
            positions_mask.append((round((x+80)*3.75), round(np.abs(y-56)*3.348)))


    for i in range(len(frames)):
        score = []
        if np.isnan(frames[i]) == False:
            if len(str(frames[i])) == 1:
                mask_path = masks[i] + '/animator_0000{}.png'.format(frames[i])
            elif len(str(frames[i])) == 2:
                mask_path = masks[i] + '/animator_000{}.png'.format(frames[i])
            im = Image.open(mask_path)

            pixels = im.load()
            #Check if the click was within the mask
            if pixels[positions_mask[i][0], positions_mask[i][1]] != (255, 255, 255) and pixels[positions_mask[i][0], positions_mask[i][1]] != (0, 0, 0):
                scores.append(1)
            else:
                scores.append(0)
        else:
            scores.append(np.nan)

    print(scores)

    for i in range(len(frames)):
        results = [base, condition, df.iat[i, 3], scores[i], df.iat[i, 1]]
        writer.writerow(results)

