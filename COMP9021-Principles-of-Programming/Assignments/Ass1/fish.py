# Written by *** for COMP9021
import os
import sys
import copy
from collections import defaultdict

filename = input('Which data file do you want to use? ')
if not os.path.exists(filename):
    print('The file does not exists')
    sys.exit()

ct_data_ol = defaultdict(list)
mi = 0
maximum = 0
with open(filename) as coast_data:
    for line in coast_data:
        strnum = line.split()
        for num in strnum:
            ct_data_ol[mi].append(int(num))
        mi += 1
min = min([ct_data_ol[i][1] for i in ct_data_ol])
max5 = 0
num_of_dic = 0
for i in ct_data_ol:
    max5 += ct_data_ol[i][1]
    num_of_dic += 1
max = max5/num_of_dic
while True:
    medium = (min+max)/2
    ct_data = copy.deepcopy(ct_data_ol)
    for i in range(len(ct_data)-1):
        if ct_data[i][1] == medium:
            continue
        elif ct_data[i][1] <medium:
            cz = medium - ct_data[i][1]
            ct_data[i][1] = medium
            distance = ct_data[i+1][0] - ct_data[i][0]
            ct_data[i+1][1] = ct_data[i+1][1] - (cz+distance)
        else:
            cz = ct_data[i][1] - medium
            ct_data[i][1] = medium
            distance = ct_data[i+1][0] - ct_data[i][0]
            if cz-distance<0:
                continue
            ct_data[i+1][1] = ct_data[i+1][1] + (cz-distance)
    ii = len(ct_data)-1
    # if medium == ct_data[ii][1]:
    if round(min) == round(max):
        maximum = int(round(medium))
        break
    elif medium < ct_data[ii][1]:
        min = medium
    else:
        max = medium
print(f'The maximum quantity of fish that each town can have is {maximum}.')

