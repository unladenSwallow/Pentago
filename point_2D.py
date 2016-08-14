# Author: Leslie Pedro
# Point class to be used with the fifteen problem.
# for TCSS 435 Programming Assignment 1
# Professor: Raghavi Sakpal

''' The point class stores an x and y coordinate on the xy plane'''
class Point:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord # the x position
        self.y = y_coord # the y position
     
    ''' Returns the point x first, then y'''   
    def get_point(self):
        return self.x, self.y
    
