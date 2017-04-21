'''
Created on Dec 26, 2016

@author: unimas
'''


class Node(object):
    __slots__ = ('type','value','children')
    
    def __init__(self,_type,_value,_children):
        self.type = _type
        self.value = _value
        self.children = _children

    def set_type(self,_type):
        self.type = _type
        
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value
    
    def get_children_count(self):
        return len(self.children)

    def get_child(self,index):
        return self.children[index]

    def get_children(self):
        return self.children

    def append_children(self,val):
        self.children.append(val)
    
    def debug(self,depth=0):
        tab = ''
        for i in range(depth):
            i = i
            tab += '\t'
        print( tab + '('+ self.get_type().name)
        if self.value != None:
            value = self.get_value()
            if type(value) != str:
                value = str(value)
            print( tab + '\t'+ value)
        if(self.children != None):
            depth += 1
            for node in self.get_children():
                node.debug(depth)
        print(tab + ')')


