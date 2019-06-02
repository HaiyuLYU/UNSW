# Randomly fills a grid of size 10 x 10 with 0s and 1s,
# in an estimated proportion of 1/2 for each,
# and computes the longest leftmost path that starts
# from the top left corner -- a path consisting of
# horizontally or vertically adjacent 1s --,
# visiting every point on the path once only.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange

from queue_adt import *


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

def find_next(pre):
    if pre == 'up':
        return ['right', 'up', 'left']
    elif pre == 'down':
        return ['left', 'down', 'right']
    elif pre == 'left':
        return ['up', 'left', 'down']
    elif pre == 'right':
        return ['down', 'right', 'up']
    else:
        return ['down', 'right']

def find_point(e):
    if e == 'up':
        return -1,0
    if e == 'down':
        return 1,0
    if e == 'left':
        return 0,-1
    if e == 'right':
        return 0,1

def leftmost_longest_path_from_top_left_corner():
    if grid[0][0] == 0:
        return []
    else:
        total_path = Queue()
        first_path = [(0, 0)]
        total_path.enqueue((first_path, 'first'))
    while True:
        if total_path.is_empty():
            break
        (path, pre) =  total_path.dequeue()
        L1 = find_next(pre)
        point = path[-1]
        for e in L1:
            pp1,pp2 = point[0],point[1]
            dp1,dp2 = find_point(e)
            np1,np2 = pp1+dp1,pp2+dp2
            if np1 < 0 or np1 >= 10:
                continue
            if np2 < 0 or np2 >= 10:
                continue
            if grid[np1][np2] == 0:
                continue
            new_point = (np1, np2)
            if new_point in path:
                continue
            else:
                if path:
                    one_path = list(path)
                    one_path.append(new_point)
                    total_path.enqueue((one_path, e))
    return path

provided_input = input('Enter one integer: ')
try:
    for_seed = int(provided_input)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(2) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
path = leftmost_longest_path_from_top_left_corner()
if not path:
    print('There is no path from the top left corner.')
else:
    print(f'The leftmost longest path from the top left corner is: {path}')

