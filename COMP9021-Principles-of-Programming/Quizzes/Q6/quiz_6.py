# Defines two classes, Point() and Triangle().
# An object for the second class is created by passing named arguments,
# point_1, point_2 and point_3, to its constructor.
# Such an object can be modified by changing one point, two or three points
# thanks to the method change_point_or_points().
# At any stage, the object maintains correct values
# for perimeter and area.
#
# Written by *** and Eric Martin for COMP9021


from math import sqrt


class PointError(Exception):
    def __init__(self, message):
        self.message = message


class Point():
    def __init__(self, x = None, y = None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is None or y is None:
            raise PointError('Need two coordinates, point not created.')
        else:
            self.x = x
            self.y = y
            
    # Possibly define other methods


class TriangleError(Exception):
    def __init__(self, message):
        self.message = message


class Triangle:
    def __init__(self, *, point_1, point_2, point_3):
        self.p1 = Point(point_1.x,point_1.y)
        self.p2 = Point(point_2.x,point_2.y)
        self.p3 = Point(point_3.x,point_3.y)
        if self.p1.y!=0 and self.p2.y!=0 and self.p3.y!=0:
            if(self.p1.x/self.p1.y)==(self.p2.x/self.p2.y)==(self.p3.x/self.p3.y):
                raise TriangleError('Incorrect input, triangle not created.')
        elif self.p1.y==0 and self.p2.y==0 and self.p3.y==0:
            raise TriangleError('Incorrect input, triangle not created.')
        a = sqrt((self.p1.x-self.p2.x)**2+(self.p1.y-self.p2.y)**2)
        b = sqrt((self.p2.x-self.p3.x)**2+(self.p2.y-self.p3.y)**2)
        c = sqrt((self.p1.x-self.p3.x)**2+(self.p1.y-self.p3.y)**2)
        p = (a+b+c)/2
        self.area =sqrt(p*(p-a)*(p-b)*(p-c))
        self.perimeter = a+b+c
    
	
    def change_point_or_points(self, *, point_1 = None,point_2 = None, point_3 = None):
        if point_1 is not None:
            self.p1 = point_1
        if point_2 is not None:
            self.p2 = point_2
        if point_3 is not None:
           	self.p3 = point_3
        flag = 0
        if self.p1.y!=0 and self.p2.y!=0 and self.p3.y!=0:
            if(self.p1.x/self.p1.y)==(self.p2.x/self.p2.y)==(self.p3.x/self.p3.y):
            	print('Incorrect input, triangle not modified.')
            	flag = 1
        elif self.p1.y==0 and self.p2.y==0 and self.p3.y==0:
            print('Incorrect input, triangle not modified.')
            flag = 1
        if flag ==0:
            a = sqrt((self.p1.x-self.p2.x)**2+(self.p1.y-self.p2.y)**2)
            b = sqrt((self.p2.x-self.p3.x)**2+(self.p2.y-self.p3.y)**2)
            c = sqrt((self.p1.x-self.p3.x)**2+(self.p1.y-self.p3.y)**2)
            p = (a+b+c)/2
            self.area =sqrt(p*(p-a)*(p-b)*(p-c))
            self.perimeter = a+b+c

    # Possibly define other methods
        

            
            

