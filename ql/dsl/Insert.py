'''
Created on Mar 14, 2017

@author: qs
'''


from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_object,parse_tok_table_name,parse_value



def parse_insert_columns(tree: Node):
    retval = []
    for e in tree.get_children():
        if e.get_type() == TK.TOK_VALUE:
            retval.append(parse_value(e))
    return retval
    
def parse_insert_row(tree: Node):
    retval = []
    for e in tree.get_children():
        if e.get_type() == TK.TOK_VALUE:
            retval.append(parse_value(e))
        elif e.get_type() in (TK.TOK_DICT,TK.TOK_LIST):
            retval.append(parse_object(e))
    return retval
    
    
class Insert(object):
    
    __slots__ = ('_index','_type','insert_columns','insert_row','metas')
    def __init__(self,tree: Node):
        self.insert_columns = []
        self.insert_row = []
        self.metas = {}
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            elif element.get_type() == TK.TOK_INSERT_COLUMNS:
                self.insert_columns = parse_insert_columns(element)
            elif element.get_type() == TK.TOK_INSERT_ROW:
                self.insert_row = parse_insert_row(element)
        for i in range(0,len(self.insert_columns)):
            if self.insert_columns[i] in ['_id','_parent','_routing','_type']:
                self.metas[self.insert_columns[i][1:]] = self.insert_row[i]
              
    def dsl(self):
        dsl_body = {}
        if len(self.insert_columns) != len(self.insert_row):
            return dsl_body
        for i in range(0,len(self.insert_columns)):
            if self.insert_columns[i] in ['_id','_parent','_routing','_type']:
                pass
            else:
                dsl_body[self.insert_columns[i]] = self.insert_row[i]
        return dsl_body
    




def parse_bulk_rows(tree: Node):
    retval = []
    for e in tree.get_children():
        retval.append(parse_insert_row(e))
    return retval


def bulk_dsl(cols,rows):
    retval = []
    for row in rows:
        bulk_row={}
        parms={'index':{}}
        if len(row) != len(cols):
            continue
        for i in range(0,len(cols)):
            if cols[i] in ['_id','_parent','_routing','_type']:
                parms['index'][cols[i]] = row[i]
            else:
                bulk_row[cols[i]] = row[i]

        retval.append(parms)
        retval.append(bulk_row)
    return retval


class Bulk(object):
    
    __slots__ = ('_index','_type','insert_columns','bulk_rows')
    def __init__(self,tree: Node):
        self.insert_columns = []
        self.bulk_rows = []
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            elif element.get_type() == TK.TOK_INSERT_COLUMNS:
                self.insert_columns = parse_insert_columns(element)
            elif element.get_type() == TK.TOK_INSERT_ROWS:
                self.bulk_rows = parse_bulk_rows(element)
              
    def dsl(self):
        dsl_body = bulk_dsl(self.insert_columns,self.bulk_rows)
        return dsl_body
    
    
    
      