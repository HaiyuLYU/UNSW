# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        if len(self) < 3:
            return
        node = self.head
        min_node = node.value
        while node:
            if node.value < min_node:
                min_node = node.value
            node = node.next_node
        node = self.head
        before_min = 0
        first_node = self.head
        og_head = self.head
        while node.next_node:
            if node.next_node.value == min_node:
                before_min = node.value
                self.head = node
            node = node.next_node
        node.next_node = og_head
        aa = self.head
        node = self.head
        while node.next_node!= aa:
            node = node.next_node
        node.next_node = None
        a1 = self.head
        even_node = self.head
        odd_node = self.head.next_node
        even_begin = even_node
        odd_begin = odd_node 
        while True:
            if even_node.next_node and even_node.next_node.next_node:
                even_node.next_node = even_node.next_node.next_node
                even_node = even_node.next_node
            else:
                break
            if odd_node.next_node and odd_node.next_node.next_node:
                odd_node.next_node = odd_node.next_node.next_node
                odd_node = odd_node.next_node
            else:
                break
        self.head = odd_begin
        even_node.next_node = None
        odd_node.next_node = even_begin
        #code for Teacher
        while self.head.next_node != a1:
            even_node = self.head
            odd_node = self.head.next_node
            begin_odd = odd_node
            while True:
                if even_node.next_node and even_node.next_node.next_node:
                    even_node.next_node = even_node.next_node.next_node
                    even_node = even_node.next_node
                else:
                    break
                if odd_node.next_node and odd_node.next_node.next_node:
                    odd_node.next_node = odd_node.next_node.next_node
                    odd_node = odd_node.next_node
                else:
                    break
            even_node.next_node = begin_odd
            odd_node.next_node = None
    
    
    
