# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for a given direction being
# one of N, E, S or W (for North, East, South or West) and for a given size greater than 1,
# the number of triangles pointing in that direction, and of that size.
#
# Triangles pointing North:
# - of size 2:
#   1
# 1 1 1
# - of size 3:
#     1
#   1 1 1
# 1 1 1 1 1
#
# Triangles pointing East:
# - of size 2:
# 1
# 1 1
# 1
# - of size 3:
# 1
# 1 1
# 1 1 1 
# 1 1
# 1
#
# Triangles pointing South:
# - of size 2:
# 1 1 1
#   1
# - of size 3:
# 1 1 1 1 1
#   1 1 1
#     1
#
# Triangles pointing West:
# - of size 2:
#   1
# 1 1
#   1
# - of size 3:
#     1
#   1 1
# 1 1 1 
#   1 1
#     1
#
# The output lists, for every direction and for every size, the number of triangles
# pointing in that direction and of that size, provided there is at least one such triangle.
# For a given direction, the possble sizes are listed from largest to smallest.
#
# We do not count triangles that are truncations of larger triangles, that is, obtained
# from the latter by ignoring at least one layer, starting from the base.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def triangles_in_grid():
    return {}
    # Replace return {} above with your code

# Possibly define other functions

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
new_dim=int((dim-1)/2)*2+dim
plus_dim=int((dim-1)/2)
def creat_new_grid():
    new_grid=[[0]*new_dim for _ in range(new_dim)]
    for i in range(dim):
        for j in range(dim):
            if grid[i][j]==0:
                new_grid[i+plus_dim][j+plus_dim]=0
            else:
                new_grid[i+plus_dim][j+plus_dim]=1
    return new_grid
new_grid=creat_new_grid();
print('Here is the grid that has been generated:')
display_grid()
# new_dim
L=list(range(1,dim+1))
newL=L[::2]
newL.pop(0)

def calculate_tr(what_grid):
    cl_grid=what_grid
    dic={}
    for i in range(plus_dim,new_dim-plus_dim):
        for j in range(plus_dim,new_dim-plus_dim):
            Flag=1
            s=0
            newL1=newL
            while cl_grid[i][j]==1 and len(newL1)!=0:
                ei=i
                s=0
                se=1
                for e in newL1:
                    se=se+1
                    ei=ei+1
                    for ej in range (j-int(e/2),j+int(e/2)+1):
                        s=s+cl_grid[ei][ej]
                    if s==sum(newL1):
                        Flag=2
                    else:
                        Flag=0
                if Flag==0:
                    newL1=newL1[:-1]
                if Flag==2:
                    if se in sorted(dic):
                        dic[se]=dic[se]+1
                    else:
                        dic[se]=1
                    break
    return dic
#number of N
new_grid_N=new_grid
n_grid=calculate_tr(new_grid_N)


#number of W
new_grid_W=new_grid
for i in range(len(new_grid_W)):
    for j in range(i+1,len(new_grid_W)):
        temp=new_grid_W[i][j]
        new_grid_W[i][j]=new_grid_W[j][i]
        new_grid_W[j][i]=temp
w_grid=calculate_tr(new_grid_W)


#number of S
new_grid_S=new_grid
for i in range(len(new_grid_S)):
    for j in range(len(new_grid_S)-i-1):
        temp=new_grid_S[i][j]
        new_grid_S[i][j]=new_grid_S[len(new_grid_S)-j-1][len(new_grid_S)-i-1]
        new_grid_S[len(new_grid_S)-j-1][len(new_grid_S)-i-1]=temp
s_grid=calculate_tr(new_grid_S)


#number of E
new_grid=creat_new_grid();
new_grid_E=new_grid
for j in range(len(new_grid_E)-1,-1,-1):
    for i in range(len(new_grid_E)-j,len(new_grid_E)):
        temp=new_grid_E[i][j]
        new_grid_E[i][j]=new_grid_E[len(new_grid_E)-1-j][len(new_grid_E)-1-i]
        new_grid_E[len(new_grid_E)-1-j][len(new_grid_E)-1-i]=temp
e_grid=calculate_tr(new_grid_E)


triangles = {'N':[],'W':[],'S':[],'E':[]}
Ln=sorted(n_grid)
Ln=sorted(Ln,reverse=True)
for i in Ln:
    if n_grid[i]!=0:
        triangles['N'].append((i,n_grid[i]))
Lw=sorted(w_grid)
Lw=sorted(Lw,reverse=True)
for i in Lw:
    if w_grid[i]!=0:
        triangles['W'].append((i,w_grid[i]))
Ls=sorted(s_grid)
Ls=sorted(Ls,reverse=True)
for i in Ls:
    if s_grid[i]!=0:
        triangles['S'].append((i,s_grid[i]))
Le=sorted(e_grid)
Le=sorted(Le,reverse=True)
for i in Le:
    if e_grid[i]!=0:
        triangles['E'].append((i,e_grid[i]))

if triangles['N']==[]:
    del triangles['N']
if triangles['W']==[]:
    del triangles['W']
if triangles['S']==[]:
    del triangles['S']
if triangles['E']==[]:
    del triangles['E']

for direction in sorted(triangles, key = lambda x: 'NESW'.index(x)):
    print(f'\nFor triangles pointing {direction}, we have:')
    for size, nb_of_triangles in triangles[direction]:
        triangle_or_triangles = 'triangle' if nb_of_triangles == 1 else 'triangles'
        print(f'     {nb_of_triangles} {triangle_or_triangles} of size {size}')

