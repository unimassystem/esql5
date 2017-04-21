'''
Created on Mar 15, 2017

@author: qs
'''


from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_tok_table_name,parse_kv
from ql.dsl.QueryBody import QueryBody,CompareExpression

def parse_update_sets(tree: Node):
    
    retval= {}
    for e in tree.get_children():
        retval.update(parse_kv(e))
    return retval
    
    
def query_body_travel(q: QueryBody,condition):

    if type(q) == CompareExpression:
        condition[q.left_values[0][1:]] = q.right_value
    else:
        if q.combine not in ['and','must']:
            return
        if hasattr(q, 'rchild'):
            query_body_travel(q.rchild,condition)
        if hasattr(q, 'lchild'):
            query_body_travel(q.lchild,condition)
    pass
    
    
def parse_conditions(tree: Node):
    query_body = QueryBody(tree.get_child(0))
    condition = {}
    query_body_travel(query_body,condition)
    return condition

class Update(object):
    __slots__ = ('_index','_type','update_sets','conditions')
    def __init__(self,tree: Node):
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            if element.get_type() == TK.TOK_SET_COLUMNS_CLAUSE:
                self.update_sets = parse_update_sets(element)
            if element.get_type() == TK.TOK_WHERE:
                self.conditions = parse_conditions(element)
                
    def dsl(self):
        return {'doc':self.update_sets}
    
    
class Upsert(Update):
    def __init__(self,tree: Node):
        Update.__init__(self,tree)
     
     
    def dsl(self):
        retval = Update.dsl(self)
        retval['doc_as_upsert'] = True
        return retval
    
    
    
    
     