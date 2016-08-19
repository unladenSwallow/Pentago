# Author: Leslie Pedro
# The Queue and Priority Queue classes to be used with the fifteen problem.
# for TCSS 435 Programming Assignment 1
# Professor: Raghavi Sakpal

''' Class for implementing a FIFO queue '''
class Queue:
    
    ''' function to initialize the class '''
    def __init__(self):
        self.queue = []
        self.size = 0
        self.max_size = 0
    
    ''' function to place a new element in the queue '''
    def put(self,new_node):
        self.queue.append(new_node)
        self.size += 1
        if self.size > self.max_size:
            self.max_size = self.size
    
    ''' function to remove an item from the queue '''
    def get(self):
        self.size -= 1
        return self.queue.pop(0)
    
    ''' Shows the value at a specific index in the Queue without removing it'''
    def peek(self, index):
        temp = self.queue.pop(index)
        self.queue.insert(index, temp)
        return temp
    
    ''' Returns true if the queue is empty, false otherwise'''
    def empty(self):
        return self.size == 0
    
    ''' Returns the number of times an element appears in the queue '''
    def count(self, char):
        return self.queue.count(char)

''' Class for implementing a Priority Queue. Elements are organized in '''
''' increasing order of total cost '''
class PriorityQueue:
    
    ''' Initializes a new priority queue '''
    def __init__(self):
        self.queue = []
        self.size = 0
        self.max_size = 0
        
    '''Function places an item in the priority queue at the proper location'''
    ''' items are placed in increasing order of the total_cost field of the '''
    ''' Node class '''
    def put(self, new_node):
        #If the queue is empty, insert new node at front
        if(self.size == 0):
            self.queue.insert(0, new_node)
        else:
            # else - search for the correct location to insert the node
            count = 0
            notIn = True
            while count < self.size:
                temp = self.queue.pop(count)
                # if the temp node from the list has a total cost that is 
                # less than the new_nodes, continue search
                if(temp.total_cost < new_node.total_cost):
                    self.queue.insert(count, temp)
                    count += 1
                # else if the temp node's total cost is greater than or equal to
                # that of the new node, place the new node in the list first, 
                # followed by the temp node and the remainder of the queue
                else :
                    self.queue.insert(count, new_node)
                    self.queue.insert(count+1, temp)
                    notIn = False #indicate that the node has been added
                    count = self.size
                # if the node was not added, it belongs at the end of the list
                if(notIn):
                    self.queue.append(new_node)
        self.size += 1 #increase the size tracker
        if self.size > self.max_size:
            self.max_size = self.size
 
    ''' gets the item at the front of the queue '''
    def get(self):
        self.size -= 1
        return self.queue.pop(0)
    
    ''' Returns true if the queue is empty, false otherwise'''
    def empty(self):
        return self.size == 0
    
    ''' Shows the element at the index provided without removing it'''
    def peek(self, index):
        temp = self.queue.pop(index)
        self.queue.insert(index, temp)
        return temp
    
    ''' Removes a state from the queue '''
    def remove(self, state):
        for count in range(0, self.size):
            if str((self.queue[count]).state) == str(state):
                self.queue.pop(count)
            self.size -= 1
    
    

''' Class for implementing a stack'''   
class Stack:
    ''' Initializes a new priority queue '''
    def __init__(self):
        self.stack = []
        self.size = 0
        self.max_size = 0

    ''' Pushes a new element onto the stack'''
    def push(self, new_node):
        self.stack.insert(0, new_node)
        self.size += 1
        if self.size > self.max_size:
            self.max_size = self.size

    ''' Pops an element off the top of the stack'''
    def pop(self):
        self.size -= 1
        return self.stack.pop(0)
    
    ''' returns true if the stack is empty and false otherwise'''
    def empty(self):
        return self.size == 0
    
    ''' shows the element at a specific index without removing it'''
    def peek(self, index):
        temp = self.stack.pop(index)
        self.stack.insert(index, temp)
        return temp