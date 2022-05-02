import yaml
import os
import copy
import numpy as np
from PIL import Image
import hashlib
from os.path import join
import shutil

# root = "/media/mika/Storage/colposcopy"
# dic = {}
# files = os.listdir(root)
# for f in files:
#     stream = open(os.path.join(root, f), 'r')
#     data = yaml.load(stream)
#     stream.close()
#     hash_key = data['file_hash']
#     version_count = len(data['versions'])
#     print(data)
#     if version_count > 1:
#         if hash_key in dic.keys():
#             dic[hash_key].append(data['versions'])
#             print("INSIDE")
#         elif version_count > 1:
#             dic[hash_key] = copy.deepcopy(data['versions'])

# with open(os.path.join(root, 'list.yaml'), 'w') as acc:
#     yaml.dump(dic, acc, default_flow_style=False)


def hasher(data_gt, batch, hashkeys={}, is_onehot=True):

    for filename, lbl in data_gt.items():
        # print(filename)
        try:
            hashed = hashlib.md5(Image.open(filename).tobytes()).hexdigest()
        except:
            print("Unable to hash: %s" % filename)
            continue
        
        if not is_onehot:
            if len(lbl) == 0:
                lbl.append("normal")
            lbl.sort()
        
        deets = {
            'filename': filename,
            'labels': '-'.join(lbl),
            'batch': batch
        }

        if hashed in hashkeys.keys():
            hashkeys[hashed]['versions'].append(deets)
            if not hashkeys[hashed]['lbl_conflict']:
                prev = None
                for ver in hashkeys[hashed]['versions']:
                    if prev is None:
                        prev = ver['labels']
                    elif ver['labels'] != prev:
                        hashkeys[hashed]['lbl_conflict'] = True
                        break
                    prev = ver['labels']
        else:
            # print(hashed)
            hashkeys[hashed] = {
                'versions' : [deets],
                'lbl_conflict' : False
            }
    # print(hashkeys)
    return copy.deepcopy(hashkeys)

def organize(d_save, hashkeys, separate=False):
    remove=[]
    ok = {}
    for key,val in hashkeys.items():
        if len(val['versions']) < 2:
            ok[key] = copy.deepcopy(val)
            remove.append(key)
    for key in remove:
        del hashkeys[key]    
    
    if separate:
        remove = []
        conflict = {}
        for key, val in hashkeys.items():
            if val['lbl_conflict']:
                remove.append(key)
                conflict[key] = copy.deepcopy(val)
        for key in remove:
            del hashkeys[key]
        with open(os.path.join(d_save, 'conflict.yaml'), 'w') as acc:
            yaml.dump(conflict, acc, default_flow_style=False)

    with open(os.path.join(d_save, 'dups.yaml'), 'w') as acc:
        yaml.dump(hashkeys, acc, default_flow_style=False)

    with open(os.path.join(d_save, 'ok.yaml'), 'w') as acc:
        yaml.dump(ok, acc, default_flow_style=False)

    if separate:
        return ok, hashkeys, conflict
    else:
        return ok, hashkeys

def to_folders(d_save, ok, dups, headers):
    label = {}
    ok.update(dups)
    counter = {}
    for key, val in ok.items():
        deets = val['versions'][0]
        batch = deets['batch']
        lbl = deets['labels']
        filename = deets['filename']
        dest = join(d_save, batch)
        if not os.path.exists(dest):
            os.makedirs(dest)
        filename2 = shutil.copy(filename, dest)
        
        if batch in label.keys():
            counter[batch] += 1
            new_name = join(dest, batch+"_{:02d}.jpg".format(counter[batch]))
            label[batch][new_name] = copy.deepcopy(lbl)

        else:
            counter[batch] = 1
            new_name = join(dest, batch+"_{:02d}.jpg".format(counter[batch]))
            label[batch] = {new_name:copy.deepcopy(lbl)}

        os.rename(filename2, new_name)
        val['versions'][0]['filename'] = new_name

    delim = '\t'
    nextl = '\n'
    for b_name, b in label.items():
        contents = 'name' + delim + delim.join(headers) + nextl
        for key, val in b.items():
            lbls = ['1' if h in val else '0' for h in headers]
            contents = contents + key + delim + delim.join(lbls) + nextl
        with open(join(join(d_save, b_name),'labels.txt'), 'w') as savehere:
            savehere.write(contents)
    with open(join(d_save, 'ok_dups_hash.yaml'), 'w') as acc:
            yaml.dump(ok, acc, default_flow_style=False)

    return counter



def negotiate_labels(items, nego_classes):
    labels = []
    tabs = []
    items = copy.deepcopy(items)
    index = None
    for j, item in enumerate(items):
        split = item['labels'].split('-')
        labels.extend([nego for nego in nego_classes if nego in split])
        lbl = [i for i in split if i not in nego_classes]
        tabs.append(len(lbl))
        if len(lbl)>0:
            index = j
        # item['labels'] = copy.deepcopy(lbl)

    if (len(tabs)-tabs.count(0))>1:
        negotiated = False
        labels = None
    else:
        negotiated = True
        labels = list(set(labels))
        if index != None:
            labels.extend(items[index]['labels'])
        labels  = '-'.join(labels)

    return negotiated, labels

    
def to_folders_conflict(d_save, conflict, headers, counter={}, nego_classes=[]):
    remove = []
    d_save = join(d_save, 'conflict')
    label = {}

    if not os.path.exists(d_save):
        os.makedirs(d_save)
    
    for key, val in conflict.items():
        negotiated, labels = negotiate_labels(val['versions'], nego_classes)
        if negotiated:
            remove.append(key)
            deets = val['versions'][0]
            batch = deets['batch']
            filename = deets['filename']
            dest = join(d_save, batch)
            if not os.path.exists(dest):
                os.makedirs(dest)
            filename2 = shutil.copy(filename, dest)

            if batch in counter.keys():
                counter[batch] += 1
            else:
                counter[batch] = 1

            if batch in label.keys():
                new_name = join(dest, batch+"_{:02d}.jpg".format(counter[batch]))
                label[batch][new_name] = copy.deepcopy(labels)

            else:
                new_name = join(dest, batch+"_{:02d}.jpg".format(counter[batch]))
                label[batch] = {new_name:copy.deepcopy(labels)}

            os.rename(filename2, new_name)
            val['versions'][0]['filename'] = new_name

    for key in remove:
        del conflict[key]    

    delim = '\t'
    nextl = '\n'
    for b_name, b in label.items():
        contents = 'name' + delim + delim.join(headers) + nextl
        for key, val in b.items():
            lbls = ['1' if h in val else '0' for h in headers]
            contents = contents + key + delim + delim.join(lbls) + nextl
        with open(join(join(d_save, b_name),'labels.txt'), 'w') as savehere:
            savehere.write(contents)
    with open(join(d_save, 'non-nego.yaml'), 'w') as acc:
            yaml.dump(conflict, acc, default_flow_style=False)


       




            




