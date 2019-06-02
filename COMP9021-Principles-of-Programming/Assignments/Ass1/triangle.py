# Written by *** for COMP9021


import os
import sys
from collections import defaultdict

filename = input('Which data file do you want to use? ')
if not os.path.exists(filename):
    print('The file does not exists')
    sys.exit()
mi = 0
tr_data = defaultdict(list)
sum_data = defaultdict(list)
count_data = defaultdict(list)
left_path = defaultdict(list)
with open(filename) as data_file:
    for line in data_file:
        number_str=line.split()
        for num in number_str:
            tr_data[mi].append(int(num))
        mi += 1

for i in range(len(tr_data)-1, -1, -1):
    for j in range(len(tr_data[i])):
        if i == len(tr_data)-1:
            sum_data[i].append(tr_data[i][j])
            count_data[i].append(1)
        else:
            if sum_data[i+1][j]>sum_data[i+1][j+1]:
                sum_data[i].append(tr_data[i][j] + sum_data[i+1][j])
                count_data[i].append(count_data[i+1][j])
            if sum_data[i+1][j]==sum_data[i+1][j+1]:
                sum_data[i].append(tr_data[i][j] + sum_data[i+1][j])
                count_data[i].append(count_data[i+1][j] + count_data[i+1][j+1])
            if sum_data[i+1][j]<sum_data[i+1][j+1]:
                sum_data[i].append(tr_data[i][j] + sum_data[i+1][j+1])
                count_data[i].append(count_data[i+1][j+1])
n = None
for i in range(0, len(sum_data)):
    for j in range(len(sum_data[i])):
        if i == 0:
            left_path[i].append(tr_data[i][j])
            n = 0
        else:
             if j==n:
                 if sum_data[i][j] == sum_data[i][j+1]:
                     left_path[i].append(tr_data[i][j])
                     n = j
                     break
                 if sum_data[i][j] < sum_data[i][j+1]:
                     left_path[i].append(tr_data[i][j+1])
                     n = j+1
                     break
                 if sum_data[i][j] > sum_data[i][j+1]:
                     left_path[i].append(tr_data[i][j])
                     n = j
                     break
jj = None
path_list = []
for i in range(0, len(left_path)):
    jj = left_path[i][0]
    path_list.append(jj)
print(f'The largest sum is: {sum_data[0][0]}')
print(f'The number of paths yielding this sum is: {count_data[0][0]}')
print(f'The leftmost path yielding this sum is: {path_list}')

