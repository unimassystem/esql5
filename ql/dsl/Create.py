'''
Created on Mar 14, 2017

@author: qs
'''


from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_object,parse_tok_table_name





class TableColumn(object):
    __slots__ = ('_column','_type','_options','properties')
    def __init__(self,tree: Node):
        self._column = tree.get_value()
        
        for e in tree.get_children():
            if e.get_type() == TK.TOK_CORE_TYPE:
                self._type = e.get_value()
            if e.get_type() == TK.TOK_COLUMN_OPTIONS:
                self._options = parse_object(e.get_child(0))
            if e.get_type() == TK.TOK_TABLE_COLUMNS:
                self.properties = parse_table_columns(e)

    def dsl(self):
        dsl_body = {}
        dsl_body[self._column] = {}
        if hasattr(self, '_type'):
            dsl_body[self._column]['type'] = self._type
        if hasattr(self, '_options'):
            dsl_body[self._column].update(self._options)
        if hasattr(self, 'properties'):
            dsl_body[self._column]['properties'] = table_columns_dsl(self.properties)
        return dsl_body




class TableMeta(object):
    __slots__ = ('_meta','_options')
    def __init__(self,tree: Node):
        self._meta = tree.get_value()
        for e in tree.get_children():
            if e.get_type() == TK.TOK_META_OPTIONS:
                self._options = parse_object(e.get_child(0))
                
    def dsl(self):
        dsl_body = {}
        dsl_body[self._meta] = {}
        if hasattr(self, '_options'):
            dsl_body[self._meta].update(self._options)
        return dsl_body

      
      
def table_columns_dsl(properties):
    retval = {}
    for e in properties:
        retval.update(e.dsl())
    return retval

            
def parse_table_columns(tree : Node):
    retval = []
    if tree.get_children() == None:
        return retval
    for e in tree.get_children():
        retval.append(TableColumn(e))
    return retval



def parse_table_metas(tree: None):
    retval = []
    if tree.get_children() == None:
        return retval
    for e in tree.get_children():
        retval.append(TableMeta(e))
    return retval
            

def table_metas_dsl(metas):
    retval = {}
    for e in metas:
        retval.update(e.dsl())
    return retval


class Create(object):
    
    __slots__ = ('_index','_type','table_columns','table_metas','_options')
    def __init__(self,tree: Node):
        
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            if element.get_type() == TK.TOK_TABLE_COLUMNS:
                self.table_columns = parse_table_columns(element)
            if element.get_type() == TK.TOK_TABLE_METAS:
                self.table_metas = parse_table_metas(element)
            if element.get_type() == TK.TOK_TABLE_OPTIONS:
                self._options = parse_object(element.get_child(0))
            else:
                self._options = {}
    
    def dsl(self):
        dsl_body = {}
        
        if hasattr(self, 'table_columns'):
            dsl_body['properties'] = table_columns_dsl(self.table_columns)
        if hasattr(self, 'table_metas'):
            dsl_body.update(table_metas_dsl(self.table_metas))
        return dsl_body
    
    
    
    