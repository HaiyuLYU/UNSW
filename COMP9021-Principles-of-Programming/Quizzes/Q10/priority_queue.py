# Written by *** for COMP9021


from binary_tree_adt import *
from math import log


class PriorityQueue(BinaryTree):
    def __init__(self):
        super().__init__()
        self.trData = [None]
        self.num = 0
    def insert(self, value):
        self.num += 1
        self.trData.append(value)
        self.value, self.left_node, self.right_node = self._bubble_up(self.num)
        
    def _bubble_up(self, num):
        if num > 1 and self.trData[num] < self.trData[num // 2]:
            temp = self.trData[num]
            self.trData[num] = self.trData[num // 2]
            self.trData[num // 2] = temp
            self._bubble_up(num // 2)
        L = []
        if len(self.trData)>=1:
            for l in self.trData[1:]:
                L.append(BinaryTree(l))
                
        for i in range(len(self.trData[1:])):
            if 2 * i + 1 < len(self.trData[1:]):
                left_tree = L[2 * i + 1]
                L[i].left_node = left_tree
            if 2 * i + 2 < len(self.trData[1:]):
                right_tree = L[2 * i + 2]
                L[i].right_node = right_tree
        return L[0].value, L[0].left_node, L[0].right_node
        
        # Replace pass above with your code
