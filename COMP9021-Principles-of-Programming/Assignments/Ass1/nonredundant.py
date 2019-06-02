# Written by *** for COMP9021

import os
import sys
import re

filename = input('Which data file do you want to use? ')
L1 = []
L2 = []
L22 = []
mi = 0
if not os.path.exists(filename):
    print('The file does not exists')
    sys.exit()
with open(filename) as po_data:
    for line in po_data:
        strnum = re.split('R|\(|\)|,',line)
        L1.append(int(strnum[2]))
        temp = [int(strnum[2]),int(strnum[3])]
        L2.append(temp)
        mi = mi +1
L1 = list(set(L1))

for m in L2:
    for n in L2:
        if m[1] == n[0] and \
            [m[0],n[1]] not in L22:
            L22.append([m[0],n[1]])
for mm in L2:
    for m in L22:
        for n in L2:
            if (m == n):
                L2.remove(m)
            else:
                if m[1] == n[0] and \
                        [m[0], n[1]] not in L22:
                    L22.append([m[0], n[1]])
newL = []
for m in L2:
	if m not in newL:
		newL.append(m)
print('The nonredundant facts are:')
for i in newL:
    print(f'R({i[0]},{i[1]})')

