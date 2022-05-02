from extractanator import get_gt_pixel, get_gt_csv, get_img_pixel, get_img_csv, get_label_pixel
from extractanator import printer
from comparanator import hasher, organize, to_folders, to_folders_conflict


##########################################################################
# FOR DATA WITH PIXEL ANNOTATION
##########################################################################

# #MIYAZAKI ANNOTATION
#(0,255,255) - AQUA - NORMAL
#(200,255,0) - YELLOW - SUSPECTED
#(0,255,0) - GREEN - TESTED
color_dict = {'sus':(200,255,0), 'check':(0,255,0)}
folder = '/media/mika/Storage/data/colpo_temp/01_miyazaki'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '01', is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/01.txt')

#ANNOTATION V2
#(0,0,255) - BLUE - NORMAL
#(0,255,255) - AQUA - LESION SUSPECTED(?)
#(0,255,0) - GREEN - DISEASE TESTED
color_dict = {'lesion':(0,255,255), 'disease':(0,255,0)}
folder = '/media/mika/Storage/data/colpo_temp/02_180607'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '02', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/02.txt')

#ANNOTATION V3
#(0,0,255) - BLUE - NORMAL
#(0,255,255) - AQUA - LESION SUSPECTED(?)
#(255,255,0) - YELLOW - CIN1
#(255,175,175) - PINK - CIN23
#(0,255,0) - GREEN - CANCER
color_dict = {'lesion':(0,255,255), 'cin1':(255,255,0), 'cin23':(255,175,175), 'cancer':(0,255,0)}
folder = '/media/mika/Storage/data/colpo_temp/03_181108'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '03', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/03.txt')

folder = '/media/mika/Storage/data/colpo_temp/04_181221'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '04', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/04.txt')

folder = '/media/mika/Storage/data/colpo_temp/05_190314'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '05', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/05.txt')

folder = '/media/mika/Storage/data/colpo_temp/06_1904-1908'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '06', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/06.txt')

folder = '/media/mika/Storage/data/colpo_temp/06_191004_reannot'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '06-2', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/06-2.txt')

folder = '/media/mika/Storage/data/colpo_temp/07_191218'
gt_dict, headers = get_gt_pixel(folder, color_dict, is_onehot=False)
data_dict = get_img_pixel(gt_dict)
hashkeys = hasher(data_dict, '07', hashkeys, is_onehot=False)
printer(data_dict, headers, '/media/mika/Storage/data/colpo_temp/07.txt')


##########################################################################
# FOR DATA WITH CSV ANNOTATION
##########################################################################
csv = '/media/mika/Storage/data/colpo/08_200528/20200513_3.csv'
root = '/media/mika/Storage/data/colpo_temp/08_200528'
gt_dict = get_gt_csv(csv, is_onehot=False, lbl_dict=['cin1', 'cin23', 'cancer'])
data_dict = get_img_csv(root, gt_dict)
hashkeys = hasher(data_dict, '08', hashkeys, is_onehot=False)
printer(data_dict, ['cin1', 'cin23', 'cancer'], '/media/mika/Storage/data/colpo_temp/08.txt')

csv = '/media/mika/Storage/data/colpo/09_200715/20200715_3.csv'
root = '/media/mika/Storage/data/colpo_temp/09_200715'
gt_dict = get_gt_csv(csv, is_onehot=False, lbl_dict=['cin1', 'cin23', 'cancer'])
data_dict = get_img_csv(root, gt_dict)
hashkeys = hasher(data_dict, '09', hashkeys, is_onehot=False)
printer(data_dict, ['cin1', 'cin2', 'cin23'], '/media/mika/Storage/data/colpo_temp/09.txt')

csv = '/media/mika/Storage/data/colpo/10_201015/2020.10.15_3.csv'
root = '/media/mika/Storage/data/colpo_temp/10_201015'
gt_dict = get_gt_csv(csv, is_onehot=False, lbl_dict=['cin1', 'cin23', 'cancer'])
data_dict = get_img_csv(root, gt_dict)
hashkeys = hasher(data_dict, '10', hashkeys, is_onehot=False)
printer(data_dict, ['cin1', 'cin23', 'cancer'], '/media/mika/Storage/data/colpo_temp/10.txt')

csv = '/media/mika/Storage/data/colpo/11_201215/2020.12.15_3.csv'
root = '/media/mika/Storage/data/colpo_temp/11_201215'
gt_dict = get_gt_csv(csv, is_onehot=False, lbl_dict=['cin1', 'cin23', 'cancer'])
data_dict = get_img_csv(root, gt_dict)
hashkeys = hasher(data_dict, '11', hashkeys, is_onehot=False)
printer(data_dict, ['cin1', 'cin23', 'cancer'], '/media/mika/Storage/data/colpo_temp/11.txt')

headers = ['cin1', 'cin23', 'cancer', 'lesion', 'disease', 'sus', 'check', 'normal']
ok, dups, conflict = organize('/media/mika/Storage/data/colpo_temp/', hashkeys, separate=True)
d_save = '/media/mika/Storage/data/colpo_temp/cleaned'
counter = to_folders(d_save, ok, dups, headers)
nego_classes=['lesion', 'disease', 'sus', 'check']
to_folders_conflict(d_save, conflict, headers, counter=counter, nego_classes=nego_classes)


