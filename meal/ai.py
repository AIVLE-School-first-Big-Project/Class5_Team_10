import torch
from PIL import Image
import numpy as np
import json

name_ko = {'roe': '알밥', 'omurice':'오므라이스', 'bibimbap':'일반비빔밥'}
model = torch.hub.load('ultralytics/yolov5', 'custom', path='meal/static/data/best_15.pt')
model.conf = 0.6

def prediction(file):
    file = Image.open(file)
    file = np.array(file)
    result = model(file)
    pp = result.pandas().xyxy[0].to_json(orient='records')
    p = json.loads(pp)
    answer = {'names': []}
    for i in p:
        answer['names'].append(name_ko[i['name']])
    return answer