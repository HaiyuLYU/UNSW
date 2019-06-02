# Randomly fills a grid of size 10 x 10 with 0s and 1s and computes:
# - the size of the largest homogenous region starting from the top left corner,
#   so the largest region consisting of connected cells all filled with 1s or
#   all filled with 0s, depending on the value stored in the top left corner;
# - the size of the largest area with a checkers pattern.
#
# Written by *** and Eric Martin for COMP9021

import sys
from random import seed, randint
import copy

dim = 10
grid = [[None] * dim for _ in range(dim)]

def display_grid():
    for i in range(dim):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

# Possibly define other functions

try:
    arg_for_seed, density = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density = int(arg_for_seed), int(density)
    if arg_for_seed < 0 or density < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
# We fill the grid with randomly generated 0s and 1s,
# with for every cell, a probability of 1/(density + 1) to generate a 0.
for i in range(dim):
    for j in range(dim):
        grid[i][j] = int(randint(0, density) != 0)
print('Here is the grid that has been generated:')
display_grid()
# -------------------------------------------------part1
grid1 = copy.deepcopy(grid)
def replace_1(i, j, n):
    global grid1
    if grid1[i][j] == n:
        grid1[i][j] = 2
        if i:
            replace_1(i - 1, j,n)
        if i < dim -1:
            replace_1(i + 1, j,n)
        if j:
            replace_1(i, j - 1,n)
        if j < dim -1:
            replace_1(i, j + 1,n)
print()
sum_size = 0
if grid1[0][0] == 0:
    replace_1(0,0,0)
else:
    replace_1(0,0,1)
for i in range(dim):
    for j in range(dim):
        if grid1[i][j] == 2:
            sum_size +=1
# ------------------------------------
# ------------------------------------part2
grid2 = copy.deepcopy(grid)
def largest_checker_pattern(i,j):
    m = grid2[i][j]
    if j and m + grid2[i][j-1] == 1:
        grid2[i][j] = 2
        largest_checker_pattern(i,j-1)
        grid2[i][j-1] =2
    if j < dim -1 and m + grid2[i][j+1] == 1:
        grid2[i][j] = 2
        largest_checker_pattern(i,j+1)
        grid2[i][j+1] = 2
    if i and m + grid2[i-1][j] == 1:
        grid2[i][j] = 2
        largest_checker_pattern(i-1,j)
        grid2[i-1][j] = 2
    if i < dim - 1 and m + grid2[i+1][j] == 1:
        grid2[i][j] = 2
        largest_checker_pattern(i+1,j)
        grid2[i+1][j] =2
    m2 = 0
    for i in range(dim):
        for j in range(dim):
            if grid2[i][j] == 2:
                m2 += 1
    return m2
max_size = 0
for i in range(dim):
    for j in range(dim):
        grid2 = copy.deepcopy(grid)
        temp = largest_checker_pattern(i,j)
        if temp > max_size:
            max_size = temp

# ------------------------------------
size_of_largest_homogenous_region_from_top_left_corner  = 0
size_of_largest_homogenous_region_from_top_left_corner = sum_size
print('The size_of the largest homogenous region from the top left corner is '
      f'{size_of_largest_homogenous_region_from_top_left_corner}.'
     )

max_size_of_region_with_checkers_structure = 0
if max_size == 0:
    max_size_of_region_with_checkers_structure = 1
else:
    max_size_of_region_with_checkers_structure = max_size
print('The size of the largest area with a checkers structure is '
      f'{max_size_of_region_with_checkers_structure}.'
     )




            

