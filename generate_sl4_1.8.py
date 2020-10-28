import json
from PIL import Image

with open('/home/tianpei.qian/workspace/data_local/sl4_front_1.0/sl4_side_val_1.7.json') as f:
    val_1_7 = json.load(f)

with open('sl4_side_val_1.7/results.json') as f:
    new_1_8 = json.load(f)

ROOT = '/home/tianpei.qian/workspace/data_local/sl4_front_1.0/'

for old, new in zip(val_1_7, new_1_8):
    assert old['file'] == new['file']
    im = Image.open(ROOT + old['file'])
    im_width, im_height = im.size
    for box in new['detections']:
        new_box = {}
        x_min, x_max, y_min, y_max = box['x_min'], box['x_max'], box['y_min'], box['y_max']
        width, height = x_max - x_min, y_max - y_min
        new_box['coord'] = [(x_min + x_max) / 2 / im_width, (y_min + y_max) / 2 / im_height, width / im_width, height / im_height]
        new_box['meta'] =  {'isfrontcar': False}
        new_box['class'] = box['kind']
        new_box['occluded'] = 'none'
        new_box['score'] = box['score']
        old['boxes'].append(new_box) 

with open('/home/tianpei.qian/workspace/data_local/sl4_front_1.0/sl4_side_val_1.8.json', 'w') as f:
    json.dump(val_1_7, f)