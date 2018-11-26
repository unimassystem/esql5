'''
Created on Mar 15, 2017

@author: qs
'''
from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_tok_table_name
from ql.dsl.QueryBody import QueryBody



class Delete(object):
    __slots__ = ('_index','_type','conditions')
    def __init__(self,tree: Node):
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            if element.get_type() == TK.TOK_WHERE:
                self.conditions = QueryBody(element.get_child(0))
                          
    def dsl(self):
        dsl_body = {}
        if hasattr(self, 'conditions'):
            dsl_body['query'] = self.conditions.dsl()
        return dsl_body
        
    
    
    