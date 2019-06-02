from collections import defaultdict
import copy
class FriezeError(Exception):
    def __init__(self, message):
        self.message = message

def ten_to_two(num_ten):
    num_str = bin(num_ten)
    num_str = num_str[2:]
    if len(num_str) == 4:
        num_two = num_str
    if len(num_str) == 3:
        num_two = '0' + num_str
    if len(num_str) == 2:
        num_two = '00' + num_str
    if len(num_str) == 1:
        num_two = '000' + num_str
    return num_two

def find_peroid(length,height,spData):
    per = 1
    per_num = length
    fir = spData[1][0]
    isOneNum = 0
    for i in range(1, height):
        for j in range(length + 1):
            if spData[i][j] != fir:
                isOneNum = 1
    if isOneNum == 0:
        return per, per_num
    else:
        for i in range(2, length + 1):
            if length % i != 0:
                continue
            l = int(length / i)
            oneP = 0
            allP = (height -1) * (i -1)
            for e in range(1, height):
                for ee in range(i-1):
                    pe = e
                    pee = ee
                    p1 = spData[e][ee * l:(ee +1) * l]
                    p2 = spData[e][(ee + 1) * l:(ee +2) * l]
                    if p1 == p2:
                        oneP += 1
            if allP == oneP:
                per = i
                per_num = int(length / i)
        return per, per_num

def N(point):
    point_two = ten_to_two(point)
    if point_two[-1] == '1':
        return True
    return False

def NE(point):
    point_two = ten_to_two(point)
    if point_two[-2] == '1':
        return True
    return False

def E(point):
    point_two = ten_to_two(point)
    if point_two[-3] == '1':
        return True
    return False

def SE(point):
    point_two = ten_to_two(point)
    if point_two[-4] == '1':
        return True
    return False

def check_horizontal(per_num, height, spData):
    lines = height + 1
    flag = True
    if (lines % 2) == 0:
        lines = int(lines / 2)
        ff = 0
    else:
        lines = int(lines / 2) + 1
    for i in range(lines):
        for j in range(per_num):
            #zhong_jian_jiao_cha
            if N(spData[i][j]):
                if not N(spData[height + 1 - i][j]):
                    flag = False
            if NE(spData[i][j]):
                if not SE(spData[height - i][j]):
                    flag = False
            if E(spData[i][j]):
                if not E(spData[height - i][j]):
                    flag = False
            if SE(spData[i][j]):
                if not NE(spData[height - i][j]):
                    flag = False
    if flag is True:
        return True
    if flag is False:
        return False

def check_glided_horizontal(per_num, height, spData):
    if (per_num % 2) == 1:
        return False
    lines = height + 1
    flag = True
    if (lines % 2) == 0:
        lines = int(lines / 2)
        ff = 0
    else:
        lines = int(lines / 2) + 1
        ff = 1
    per_num2 = int(per_num / 2)
    for i in range(lines):
        for j in range(int(per_num)):
            if N(spData[i][j]):
                if not N(spData[height + 1 - i][j + per_num2]):
                    flag = False
            if NE(spData[i][j]):
                if not SE(spData[height - i][j + per_num2]):
                    flag = False
            if E(spData[i][j]):
                if not E(spData[height - i][j + per_num2]):
                    flag = False
            if ff == 1 and i == lines - 1 and SE(spData[i][j]):
                continue
            if SE(spData[i][j]):
                if not NE(spData[height - i][j + per_num2]):
                    flag = False
    if flag is True:
        return True
    if flag is False:
        return False

def check_if_vertical(per_num, height, spData, ff):
    flag = True
    flag2 = 0
    check_again_k = None
    if (per_num % 2) == 0:
        column = int(per_num / 2)
    else:
        column = int(per_num / 2) + 1
    for k in range(per_num):
        for i in range(height + 1):
            if N(spData[i][k + column -1]) or  N(spData[i][k + column +1]):
                zj = 0
                break
            else:
                zj = 1
        for i in range(height + 1):
            if ff == 0:
                m = 0
            if ff == 1:
                m = 1
            for j in range(k, k + column):
                if N(spData[i][j]):
                    if not N(spData[i][(k + per_num) - m - zj]):
                        flag = False
                if NE(spData[i][j]):
                    if not SE(spData[i - 1][(k + per_num - 1) - m]):
                        flag = False
                if E(spData[i][j]):
                    if not E(spData[i][(k + per_num - 1) - m]):
                        flag = False
                if SE(spData[i][j]):
                    if not NE(spData[i + 1][(k + per_num - 1) - m]):
                        flag = False
                m = m + 1
        if flag is False:
            flag = True
            continue
        else:
            flag2 = 1
            break
    if flag2 == 1:
        return True
    else:
        return False

def check_vertical(per_num, height, spData):
    if check_if_vertical(per_num, height, spData, 1):
        return True
    elif check_if_vertical(per_num, height, spData, 0):
        return True
    else:
        return False

def check_rotation (per_num, height, length, spData):
    lines = height + 1
    flag2 = 0
    flag = True
    if (lines % 2) == 0:
        lines = int(lines / 2)
        ff = 0
    else:
        lines = int(lines / 2) + 1
        ff = 1
    per_num2 = int(per_num)
    for k in range(per_num2):
        for i in range(lines):
            for j in range(per_num2):
                if N(spData[i][j]):
                    if not N(spData[height - i + 1][(per_num - 1) - j + 1 + k]):
                        flag = False
                if NE(spData[i][j]):
                    if not NE(spData[height - i + 1][(per_num - 1) - j + k]):
                        flag = False
                if E(spData[i][j]):
                    if not E(spData[height - i][(per_num - 1) - j + k ]):
                        flag = False
                if ff == 1 and i == lines - 1 and SE(spData[i][j + k]):
                    continue
                if SE(spData[i][j]):
                    if not SE(spData[height - i - 1][(per_num - 1) - j + k]):
                        flag = False
        if flag is False:
            flag = True
            continue
        else:
            flag2 = 1
            break
    if flag2 == 1:
        return True
    else:
        return False
def print_N(spData,height,length):
    begin = None
    end = None
    pn = defaultdict(list)
    ii = 0
    for j in range(length + 1):
        for i in range(height + 1):
            if begin == None:
                if N(spData[i][j]):
                    begin = (j, i - 1)

            else:
                if not N(spData[i][j]):
                    end = (j, i - 1)
                    if end[1] == -1:
                        end =(j - 1, height)
            if begin != None and end == None and j == length and i == height:
                end = (j, i)
            if begin != None and end != None:
                pn[ii].append(begin)
                pn[ii].append(end)
                begin = None
                end = None
                ii += 1
    return pn
def print_SE(spData,height,length):
    cpData = copy.deepcopy(spData)
    begin = None
    end = None
    pse = defaultdict(list)
    ii = 0
    for i in range(height + 1):
        for j in range(length + 1):
            m = i
            n = j
            if begin == None:
                if SE(cpData[i][j]):
                    begin = (j, i)
                    end = (j + 1, i + 1)
                    cpData[i][j] = 0
                    while True:
                        i += 1
                        j += 1
                        if SE(cpData[i][j]):
                            end = (j + 1, i + 1)
                            cpData[i][j] = 0
                        else:
                            break
            i = m
            j = n
            if begin != None and end != None:
                pse[ii].append(begin)
                pse[ii].append(end)
                begin = None
                end = None
                ii += 1
    return pse
def print_E(spData,height,length):
    begin = None
    end = None
    pe = defaultdict(list)
    ii = 0
    for i in range(height + 1):
        for j in range(length + 1):
            if begin == None:
                if E(spData[i][j]):
                    begin = (j, i)
            else:
                if not E(spData[i][j]):
                    end = (j, i)
            if begin != None and end != None:
                pe[ii].append(begin)
                pe[ii].append(end)
                begin = None
                end = None
                ii += 1
    return pe
def print_NE(spData,height,length):
    cpData = copy.deepcopy(spData)
    begin = None
    end = None
    pse = defaultdict(list)
    ii = 0
    for i in range(height + 1):
        for j in range(length + 1):
            m = i
            n = j
            if begin == None:
                if NE(cpData[i][j]):
                    begin = (j + 1, i - 1)
                    end = (j, i)
                    cpData[i][j] = 0
                    while True:
                        if j - 1 == -1:
                            break
                        if i + 1 == height + 1:
                            break
                        i += 1
                        j -= 1
                        if NE(cpData[i][j]):
                            end = (j, i)
                            cpData[i][j] = 0
                        else:
                            break
            i = m
            j = n
            if begin != None and end != None:
                temp = begin
                begin = end
                end = temp
                pse[ii].append(begin)
                pse[ii].append(end)
                begin = None
                end = None
                ii += 1
    L1 = []
    L2 = []
    for i in pse:
        L1.append(pse[i][0][0])
        L2.append(pse[i][0][1])
    L11 = list(set(L1))
    L11.sort()
    L22 = list(set(L2))
    L22.sort()
    pse2 = defaultdict(list)
    iii = 0
    for m in L22:
        for n in L11:
            for k in pse:
                if n == pse[k][0][0] and m == pse[k][0][1]:
                    pse2[iii].append(pse[k][0])
                    pse2[iii].append(pse[k][1])
                    iii = iii + 1
    return pse2
class Frieze:
    def __init__(self,fileName):
        fileName = str(fileName)
        self.fileName = fileName[:-4]
        self.spData = defaultdict(list)
        self.mi = 0
        with open(fileName) as dataFile:
            for line in dataFile:
                number_str = line.split()
                if len(number_str) == 0:
                    continue
                for num in number_str:
                    if int(num) not in range(0,16):
                        raise FriezeError('Incorrect input.')
                    self.spData[self.mi].append(int(num))
                self.mi += 1
        # Incorrect input.
        fL = len(self.spData[0])
        for i in self.spData:
            oneL = len(self.spData[i])
            if oneL < fL or oneL > fL:
                raise FriezeError('Incorrect input.')
        self.length = len(self.spData[0]) - 1
        self.height = len(self.spData) - 1
        if self.length < 4 or self.length > 50:
            raise FriezeError('Incorrect input.')
        if self.height < 2 or self.height > 16:
            raise FriezeError('Incorrect input.')
        # Input does not represent a frieze.
        #top
        for i in range(self.length):
            str_e = ten_to_two(self.spData[0][i])
            if str_e[-3] != '1':
                raise FriezeError('Input does not represent a frieze.')
            if str_e[-1] == '1' or str_e[-2] == '1':
                raise FriezeError('Input does not represent a frieze.')
        #bot
        for i in range(self.length):
            str_e = ten_to_two(self.spData[self.height][i])
            if str_e[-3] != '1':
                raise FriezeError('Input does not represent a frieze.')
            if str_e[-4] == '1':
                raise FriezeError('Input does not represent a frieze.')
        #left
        # for i in range(1, self.height):
        #     str_e = ten_to_two(self.spData[i][0])
        #     if self.spData[i][0] == 0:
        #         continue
        #     if str_e[-1] != '1':
        #         raise inputError('Input does not represent a frieze.5')
        #right
        for i in range(self.height + 1):
            int_e = self.spData[i][-1]
            if int_e not in [0, 1]:
                raise FriezeError('Input does not represent a frieze.')
        # conditionX
        for i in range(self.height):
            for j in range(self.length + 1):
                str_e1 = ten_to_two(self.spData[i][j])
                str_e2 = ten_to_two(self.spData[i+1][j])
                if str_e1[-4] == '1' and str_e2[-2] == '1':
                    # print(str_e1)
                    # print(str_e2)
                    raise FriezeError('Input does not represent a frieze.')
        # conditionX bot
        for j in range(self.length + 1):
            str_e1 = ten_to_two(self.spData[self.height - 1][j])
            str_e2 = ten_to_two(self.spData[self.height][j])
            if str_e1[-4] == '1' and str_e2[-2] == '1':
                raise FriezeError('Input does not represent a frieze.')
        # find period
        self.period,self.per_num = find_peroid(self.length,self.height,self.spData)
        if self.period == 1:
            raise FriezeError('Input does not represent a frieze.')

    def analyse(self):
        horizontal = check_horizontal(self.per_num, self.height, self.spData)
        vertical = check_vertical(self.per_num, self.height, self.spData)
        glided_horizontal = check_glided_horizontal(self.per_num, self.height, self.spData)
        rotation = check_rotation(self.per_num, self.height, self.length, self.spData)
        # if horizontal:
        #     print('horizontal')
        # if vertical:
        #     print('vertical')
        # if glided_horizontal:
        #     print('glided_horizontal')
        # if rotation:
        #     print('rotation')
        # if flag == 1:
        #     print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation only.')
        if horizontal and vertical and rotation:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation,')
            print('        horizontal and vertical reflections, and rotation only.')
        elif glided_horizontal and vertical and rotation:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation,')
            print('        glided horizontal and vertical reflections, and rotation only.')
        elif rotation:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation')
            print('        and rotation only.')
        elif glided_horizontal:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation')
            print('        and glided horizontal reflection only.')
        elif horizontal:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation')
            print('        and horizontal reflection only.')
        elif vertical:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation')
            print('        and vertical reflection only.')
        else:
            print(f'Pattern is a frieze of period {self.per_num} that is invariant under translation only.')
    def display(self):
        pn = print_N(self.spData, self.height, self.length)
        pe = print_E(self.spData, self.height, self.length)
        pse = print_SE(self.spData, self.height, self.length)
        pne = print_NE(self.spData, self.height, self.length)
        with open(f'{self.fileName}.tex', 'w') as tex:
            print('\\documentclass[10pt]{article}', file=tex)
            print('\\usepackage{tikz}', file=tex)
            print('\\usepackage[margin=0cm]{geometry}', file = tex)
            print('\\pagestyle{empty}\n', file=tex)
            print('\\begin{document}\n', file=tex)
            print('\\vspace*{\\fill}', file=tex)
            print('\\begin{center}', file=tex)
            print('\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]', file=tex)
            print('% North to South lines', file=tex)
            for i in range(len(pn)):
                print(f'    \draw ({pn[i][0][0]},{pn[i][0][1]}) -- ({pn[i][1][0]},{pn[i][1][1]});', file=tex)
            print('% North-West to South-East lines', file=tex)
            for i in pse:
                print(f'    \draw ({pse[i][0][0]},{pse[i][0][1]}) -- ({pse[i][1][0]},{pse[i][1][1]});', file=tex)
            print('% West to East lines', file=tex)
            for i in range(len(pe)):
                print(f'    \draw ({pe[i][0][0]},{pe[i][0][1]}) -- ({pe[i][1][0]},{pe[i][1][1]});', file=tex)
            print('% South-West to North-East lines', file=tex)
            for i in range(len(pne)):
                print(f'    \draw ({pne[i][0][0]},{pne[i][0][1]}) -- ({pne[i][1][0]},{pne[i][1][1]});', file=tex)
            print('\\end{tikzpicture}', file=tex)
            print('\\end{center}', file=tex)
            print('\\vspace*{\\fill}\n', file=tex)
            print('\\end{document}', file=tex)

