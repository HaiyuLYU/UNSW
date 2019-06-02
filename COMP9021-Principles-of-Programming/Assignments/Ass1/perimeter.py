import os
import sys
from collections import defaultdict

filename = input('Which data file do you want to use? ')
if not os.path.exists(filename):
    print('The file does not exists')
    sys.exit()
mi = 0
tr_data = defaultdict(list)
with open(filename) as data_file:
    for line in data_file:
        number_str=line.split()
        for num in number_str:
            tr_data[mi].append(int(num))
        mi += 1
xa_sum = 0

for i in tr_data:
    if tr_data[i][0]<tr_data[i][2]:
        xa_min = tr_data[i][0]
        xa_max = tr_data[i][2]
    else:
        xa_max = tr_data[i][0]
        xa_min = tr_data[i][2]
    ya = tr_data[i][1]
    for xa in range(xa_min,xa_max+1):
        flag=0
        for ii in tr_data:
            if xa<tr_data[ii][2] and \
                xa>=tr_data[ii][0] and \
                ya<tr_data[ii][3] and \
                ya>tr_data[ii][1]:
                flag=1
                break
        if flag == 1:
            continue
        if xa == xa_max:
            break
        xa_sum = xa_sum+1
# print(xa_sum)

xb_sum = 0
for i in tr_data:
    if tr_data[i][0]<tr_data[i][2]:
        xb_min = tr_data[i][0]
        xb_max = tr_data[i][2]
    else:
        xb_max = tr_data[i][0]
        xb_min = tr_data[i][2]
    yb = tr_data[i][3]
    for xb in range(xb_min,xb_max+1):
        flag=0
        for ii in tr_data:
            if xb<tr_data[ii][2] and \
                xb>=tr_data[ii][0] and \
                yb<tr_data[ii][3] and \
                yb>tr_data[ii][1]:
                flag=1
                break
        if flag == 1:
            continue
        if xb == xb_max:
            break
        xb_sum = xb_sum+1
# print(xb_sum)

ya_sum = 0
for i in tr_data:
    if tr_data[i][1]<tr_data[i][3]:
        ya_min = tr_data[i][1]
        ya_max = tr_data[i][3]
    else:
        ya_max = tr_data[i][1]
        ya_min = tr_data[i][3]
    xa = tr_data[i][0]
    for ya in range(ya_min,ya_max+1):
        flag=0
        for ii in tr_data:
            if xa<tr_data[ii][2] and \
                xa>tr_data[ii][0] and \
                ya<tr_data[ii][3] and \
                ya>=tr_data[ii][1]:
                flag=1
                break
        if flag == 1:
            continue
        if ya == ya_max:
            break
        ya_sum = ya_sum+1
# print(ya_sum)

yb_sum = 0
for i in tr_data:
    if tr_data[i][1]<tr_data[i][3]:
        yb_min = tr_data[i][1]
        yb_max = tr_data[i][3]
    else:
        yb_max = tr_data[i][1]
        yb_min = tr_data[i][3]
    xb = tr_data[i][2]
    for yb in range(yb_min,yb_max+1):
        flag=0
        for ii in tr_data:
            if xb<tr_data[ii][2] and \
                xb>tr_data[ii][0] and \
                yb<tr_data[ii][3] and \
                yb>=tr_data[ii][1]:
                flag=1
                break
        if flag == 1:
            continue
        if yb == yb_max:
            break
        yb_sum = yb_sum+1
# print(yb_sum)
sum4=xa_sum+xb_sum+ya_sum+yb_sum
print(f'The perimeter is: {sum4}')

