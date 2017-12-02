from load_data import *
import json
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import os
IMAGE_DIR = 'image_feature'
PIC_DIR = 'pic'
def _image():
    data = load_data()
    data = data[:len(data)/3]
    each_image_stat = {}

    features = ['number_of_upvotes','number_of_downvotes','number_of_comments']
    for record in data:
        image_id = record.get('image_id')
        if image_id not in each_image_stat:
            each_image_stat[image_id] = defaultdict(float)
        for feature in features:
            each_image_stat[image_id]['avg_'+feature] += float(record.get(feature))
        each_image_stat[image_id]['num_of_posts'] += 1
    
    for image_id,stat in each_image_stat.items():
        for feature in features:
            each_image_stat[image_id]['avg_'+feature] /= each_image_stat[image_id]['num_of_posts']
        each_image_stat[image_id] = dict(each_image_stat[image_id])

    number_of_upvotes_list = [int(record.get('number_of_upvotes')) for record in data]
    number_of_downvotes_list = [int(record.get('number_of_downvotes')) for record in data]
    number_of_comments_list = [int(record.get('number_of_comments')) for record in data]

    overall_stat = {
        'avg_number_of_upvotes': np.mean(number_of_upvotes_list),
        'avg_number_of_downvotes': np.mean(number_of_downvotes_list),
        'avg_number_of_comments': np.mean(number_of_comments_list),
        'std_number_of_upvotes': np.std(number_of_upvotes_list),
        'std_number_of_downvotes': np.std(number_of_downvotes_list),
        'std_number_of_comments': np.std(number_of_comments_list)
    }

    with open(os.path.join(IMAGE_DIR,'each_image_stat.json'),'w') as fp:
        json.dump(dict(each_image_stat),fp)
    with open(os.path.join(IMAGE_DIR,'overall_stat.json'),'w') as fp:
        json.dump(overall_stat,fp)



if __name__ == '__main__':
    _image()


    