import os
from os.path import join
import yaml
import shutil

def get_name(full):
    return full.split(os.sep)[-1].split('.')[0]

start = ['01', '02', '03', '04', '05', '06', '06-2', '07']
dest = "/media/mika/Storage/data/colpo_temp/cleaned/gt"
y_cleaned = "/media/mika/Storage/data/colpo_temp/cleaned/ok_dups_hash.yaml"
# y_all = "/media/mika/Storage/data/colpo_temp/ok.yaml"
y_all = "/media/mika/Storage/data/colpo_temp/dups.yaml"

stream = open(y_cleaned, 'r')
data_cleaned = yaml.load(stream)
stream.close()

stream = open(y_all, 'r')
data_all = yaml.load(stream)
stream.close()

for hash1, val1 in data_cleaned.items():
    for item in val1['versions']:
        if item['batch'] in start:
            name1 = get_name(item['filename'])
            for hash2, val2 in data_all.items():
                if hash1 == hash2:
                    for item2 in val2['versions']:
                        if item2['batch'] in start:
                            gt = item2['filename'].replace(".jpg","_gt.png")
                            filename2 = shutil.copy(gt, join(dest, name1+".png"))
                            break
                    break
        
        
