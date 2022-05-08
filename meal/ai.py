import torch
from PIL import Image
import numpy as np
import json

model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path='meal/static/data/last_weight.pt')
model.conf = 0.1


def prediction(file):
    file = Image.open(file)
    file = np.array(file)
    result = model(file)
    pp = result.pandas().xyxy[0].to_json(orient='records')
    p = json.loads(pp)
    answer = {'names': []}
    for i in p:
        answer['names'].append(i['name'])
    return answer
