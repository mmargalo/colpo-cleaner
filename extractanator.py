import os
from os.path import join
import cv2
import re

def get_label_pixel(path, color_dict, is_onehot=True):
    """
    Pixel annotation -> one-hot vector
    """    
    label = []
    try:
        img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    except:
        print("Could not open file %s" % path)
    
    for idx in color_dict.keys():
        color = color_dict.get(idx)
        contains = True if 255 in cv2.inRange(img, color, color) else False
        if is_onehot:
            if contains:
                label.append("1")
            else:
                label.append("0")
        elif contains:
            label.append(idx)
    if len(label)<1 and not is_onehot:
        label.append('normal')
    return label

def get_gt_pixel(folder, color_dict, is_onehot=True):
    """
    Extracts labels from GT pixels
    Returns: dict(gt_path=label), color_dict.keys()
    """
    gt_img = []
    gt_dict = {}

    for root, dirs, files in os.walk(folder):
        paths = [join(root, f) for f in files if  f.endswith('gt.png')]
        for path in paths:
            label = get_label_pixel(path, color_dict, is_onehot)
            path = path.replace('_gt.png', '')
            if path not in gt_dict.keys():
                gt_dict[path] = label
            else:
                print("Duplicate GT: %s" % path)

    return gt_dict, color_dict.keys()

def get_img_pixel(gt_dict):
    """
    Param: gt_dct - dict(gt_path=label)
    Returns: dict(img_path=label)
    Assumes gt and img are in the same dir
    """
    data_dict = {}
    for name, label in gt_dict.items():
        name = name + '.jpg'
        if os.path.exists(name):
            if name not in data_dict.keys():
                data_dict[name] = label
            else:
                print("Duplicate image: %s" % name)
        else:
            print("Non-exsistent: %s" % name)
    return data_dict


def get_gt_csv(path, is_onehot=True, lbl_dict=None):
    """
    Extracts labels from GT csv
    Returns: dict(gt_path=label), list(headers)
    """
    gt_dict = {}
    if not is_onehot:
        if lbl_dict is None:
            print("Missing headers")
            return gt_dict

    with open(path, 'r') as csv:
        lines = csv.readlines()
        lines = [line.strip() for line in lines]
        # header = lines[0].split()[1:]
        # for line in lines[1:]:
        for line in lines:
            line_split = line.split()
            name = line_split[0]
            lbl = line_split[1:]
            if not is_onehot:
                lbl = [lbl_dict[i] for i,l in enumerate(lbl) if int(l)==1 ]
                if len(lbl) < 1:
                    lbl = ['normal']
            if name not in gt_dict.keys():
                gt_dict[name] = lbl
            else:
                print("Duplicate GT: %s" % name)
    return gt_dict#, headers

def get_img_csv(root, gt_dict):
    """
    Param: root - root directory to search in; gt_dict - dict(img_root_name=label)
    Returns: dict(img_path=label)
    """
    data_dict = {}
    dir_dict = {}
    #dir_root = {re.sub(r'_\d+', "", key):[key.split('_')[-1]] if not dir_root[re.sub(r'_\d+', "", key)] else re.sub(r'_\d+', "", key): dir_root[re.sub(r'_\d+', "", key)].append(key.split('_')[-1]) for key in gt_dict.keys()}
    unique = [re.sub(r'_\d+', "", key) for key in gt_dict.keys()]
    unique = list(set(unique))
    for key in gt_dict.keys():
        dir_root = re.sub(r'_\d+', "", key)
        if dir_root in dir_dict.keys():
            dir_dict[dir_root].append(key.split('_')[-1])
        else:
            dir_dict[dir_root] = [key.split('_')[-1]]

    for root, dirs, files in os.walk(root):
        for d in dirs:
            if d in unique:
                # occur = [key for key in gt_dict.keys() if d in key]
                occur = dir_dict[d]
                for occ in occur:
                    name = d  + '_' + occ
                    # Consider the common name variations in the current dataset
                    name1 = join(join(root, d), d + '_' + occ + '.jpg')                                                                                    
                    name2 = join(join(root, d), d + ' (' + occ + ').jpg')
                    name3 = join(join(root, d), occ + '.jpg')
                    if os.path.exists(name1):
                        data_dict[name1] = gt_dict[name]
                    elif os.path.exists(name2):
                        data_dict[name2] = gt_dict[name]
                    elif os.path.exists(name3):
                        data_dict[name3] = gt_dict[name]
                    else:
                        print("Cannot find image for %s" % name1)
            else:
                print("Directory has no labels: %s" % d)
    return data_dict

def printer(img_dict, headers, d_save):
    sep = '\t'
    nextl = '\n'
    content = 'name' + sep + sep.join(headers) + nextl
    for img, lbl in img_dict.items():
        content = content + img + sep + sep.join(lbl) + nextl 
    with open(d_save, 'w+') as writer:
        writer.write(content)
