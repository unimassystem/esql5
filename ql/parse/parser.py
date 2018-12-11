'''
Created on Dec 15, 2016

@author: qs
'''

from ql.parse import lexer
from ql.parse import ASTNode
from enum import Enum

class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    
    
    
class TK(AutoNumber):
    TOK_IDENTIFIER = ()
    TOK_VALUE = ()
    TOK_DQ_VALUE = ()
    TOK_DOT = ()
    TOK_LIST = ()
    TOK_DICT = ()
    TOK_TUPLE = ()
    TOK_KEY_VALUE = ()
    
    TOK_CORE_TYPE = ()
    TOK_TABLE_NAME=()
    
    TOK_CREATE_TABLE = ()
    TOK_QUERY = ()
    TOK_INSERT_INTO = ()
    TOK_BULK_INTO = ()
    TOK_UPSERT_INTO = ()
    TOK_UPDATE = ()
    TOK_DELETE = ()
    
    TOK_COLUMN_DEFINE = ()
    TOK_COLUMN_OPTIONS = ()
    TOK_META_DEFINE = ()
    TOK_META_OPTIONS = ()
    TOK_TABLE_COLUMNS = ()
    TOK_TABLE_METAS = ()
    TOK_TABLE_OPTIONS = ()
    
    TOK_FUNCTION = ()
    TOK_EXPRESSION = ()
    TOK_COMPARE = ()
    TOK_IN = ()
    TOK_REVERSED = ()
    TOK_COMPOUND = ()
    TOK_EXPRESSION_LEFT = ()
    TOK_EXPRESSION_RIGHT = ()

    TOK_SELECT = ()
    TOK_SELEXPR = ()
    TOK_FROM = ()
    TOK_WHERE = ()
    TOK_LIMIT = ()
    TOK_ORDERBY = ()
    TOK_GROUPBY = ()
    TOK_SORT = ()
    TOK_SORT_MODE = ()
    
    TOK_INSERT_COLUMNS = ()
    TOK_INSERT_ROW = ()
    TOK_INSERT_ROWS = ()
    
    TOK_SET_COLUMNS_CLAUSE = ()
    
    TOK_EXPLAIN = ()
    
    TOK_DESC_TABLE = ()
    TOK_SHOW_TABLES = ()
    TOK_DROP_TABLE = ()

tokens = lexer.tokens

precedence = (
              ('left','OR'),
              ('left','AND'),
              ('left','NOT'))


def token_list(plist):
    retval = []
    if len(plist) == 2:
        retval = [plist[1]]
    else:
        if isinstance(plist[3],list):
            retval = [plist[1]] + plist[3]
        else:
            retval = [plist[1],plist[3]]    
    return retval


def p_EXECUTE_STATEMENT(p):
    '''EXECUTE_STATEMENT : STATEMENT'''
    p[0] = p[1]   
    
    
def p_EXPLAIN_STATEMENT(p):
    '''STATEMENT : EXPLAIN STATEMENT'''
    p[0] = ASTNode.Node(TK.TOK_EXPLAIN,None,[p[2]])
    
    
def p_STATEMENT(p):
    '''STATEMENT : TOK_CREATE_TABLE
    | TOK_INSERT_INTO
    | TOK_QUERY
    | TOK_BULK_INTO
    | TOK_UPDATE
    | TOK_UPSERT_INTO
    | TOK_DELETE
    | TOK_SHOW_TABLES
    | TOK_DESC_TABLE
    | TOK_DROP_TABLE'''
    p[0] = p[1]



'''======================================base define========================================================'''


def p_TOK_OPTIONS_OBJECT(p):
    '''TOK_OPTIONS_OBJECT : "(" KV_ELEMENTS_EXPR ")"'''
    p[0] = ASTNode.Node(TK.TOK_DICT,None,p[2])


def p_TOK_DICT_OBJECT(p):
    '''TOK_DICT_OBJECT : "{" KV_ELEMENTS_EXPR "}"'''
    p[0] = ASTNode.Node(TK.TOK_DICT,None,p[2])


def p_TOK_LIST_OBJECT(p):
    '''TOK_LIST_OBJECT : "[" VALUES_EXPR "]"
    | "[" "]"'''
    if len(p) == 4:
        p[0] = ASTNode.Node(TK.TOK_LIST,None,p[2])
    else:
        p[0] = ASTNode.Node(TK.TOK_LIST,None,None)


def p_TOK_TUPLE_OBJECT(p):
    '''TOK_TUPLE_OBJECT : "(" VALUES_EXPR ")"
    | "(" ")"'''
    if len(p) == 4:
        p[0] = ASTNode.Node(TK.TOK_TUPLE,None,p[2])
    else:
        p[0] = ASTNode.Node(TK.TOK_TUPLE,None,None)
        
    
def p_KV_ELEMENTS_EXPR(p):
    '''KV_ELEMENTS_EXPR : TOK_KEY_VALUE
    | TOK_KEY_VALUE COMMA TOK_KEY_VALUE
    | TOK_KEY_VALUE COMMA KV_ELEMENTS_EXPR'''
    p[0] = token_list(p)                 


def p_VALUES_EXPR(p):
    '''VALUES_EXPR : VALUE_EXPR
    | VALUE_EXPR COMMA VALUE_EXPR
    | VALUE_EXPR COMMA VALUES_EXPR'''
    p[0] = token_list(p)
            

def p_TOK_KEY_VALUE(p):
    '''TOK_KEY_VALUE : TOK_EXPRESSION'''
    if p[1].get_value() != '=':
        pass
    else:
        p[0] = p[1]
    p[0].set_type(TK.TOK_KEY_VALUE)



def p_LEFT_RESERVED_VALUES_EXPR(p):
    '''LEFT_RESERVED_VALUES_EXPR :  FROM
    | TO'''
    p[0] = ASTNode.Node(TK.TOK_VALUE,p[1],None)


 
def p_LEFT_VALUE_EXPR(p):
    '''LEFT_VALUE_EXPR :  VALUE_EXPR
    | TOK_FUNCTION_EXPR
    | LEFT_RESERVED_VALUES_EXPR'''
    p[0] = p[1]

def p_LEFT_VALUES_EXPR(p):
    '''LEFT_VALUES_EXPR :  LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR COMMA LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR COMMA LEFT_VALUES_EXPR'''
    p[0] = token_list(p)
         
   
def p_RIGHT_VALUE_EXPR(p):
    '''RIGHT_VALUE_EXPR :  VALUE_EXPR'''
    p[0] = p[1]    


def p_RIGHT_VALUES_EXPR(p):
    '''RIGHT_VALUES_EXPR :  VALUE_EXPR
    | RIGHT_VALUE_EXPR COMMA RIGHT_VALUE_EXPR
    | RIGHT_VALUE_EXPR COMMA RIGHT_VALUES_EXPR'''
    p[0] = token_list(p)
    
    

def p_VALUE_EXPR(p):
    '''VALUE_EXPR :  TOK_DOT
    | TOK_VALUE
    | TOK_DICT_OBJECT
    | TOK_LIST_OBJECT'''
    p[0] = p[1]


def p_TOK_DOT(p):
    '''TOK_DOT : TOK_VALUE "." TOK_VALUE
    | TOK_VALUE "." TOK_DOT'''
    p[0] = ASTNode.Node(TK.TOK_DOT,p[2],[p[1],(p[3])])


def p_TOK_DQ_VALUE(p):
    '''TOK_VALUE : DQUOTE_STRING'''
    p[0] = ASTNode.Node(TK.TOK_VALUE,p[1],[ASTNode.Node(TK.TOK_DQ_VALUE,None,None)]) 
    
       
def p_TOK_VALUE(p):
    '''TOK_VALUE : WORD
    | QUOTE_STRING
    | NUMBER
    | "*"'''
    p[0] = ASTNode.Node(TK.TOK_VALUE,p[1],None)
 


def p_TOK_WILDCARD_VALUE(p):
    '''TOK_VALUE : WORD "*"'''
    p[0] = ASTNode.Node(TK.TOK_VALUE,p[1] + p[2],None)
     
           
'''=======================================operator define=============================================='''

 
def p_EXPRESSIONS_REVERSED_EXPR(p):
    '''EXPRESSION_EXPR : NOT EXPRESSION_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_REVERSED,p[1].lower(),[p[2]])
    

def p_EXPRESSIONS_GROUP_EXPR(p):
    '''EXPRESSION_EXPR : "(" EXPRESSION_EXPR ")"'''
    p[0] = p[2]


def p_EXPRESSION_OPERATOR_EXPR(p):
    '''EXPRESSION_EXPR :  EXPRESSION_EXPR OR EXPRESSION_EXPR
    | EXPRESSION_EXPR AND EXPRESSION_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_COMPOUND,p[2].lower(),[p[1],p[3]])



def p_EXPRESSION_EXPR(p):
    '''EXPRESSION_EXPR : TOK_EXPRESSION
    | TOK_FUNCTION_EXPR
    | TOK_IN_EXPR'''
    p[0] = p[1]
    
    
def p_TOK_EXPRESSION_LEFT(p):
    '''TOK_EXPRESSION_LEFT : LEFT_VALUES_EXPR'''
    p[0] =  ASTNode.Node(TK.TOK_EXPRESSION_LEFT,None,p[1])
    
def p_TOK_EXPRESSION_RIGHT(p):
    '''TOK_EXPRESSION_RIGHT : RIGHT_VALUE_EXPR'''
    p[0] =  ASTNode.Node(TK.TOK_EXPRESSION_RIGHT,None,[p[1]])
        
def p_TOK_EXPRESSION(p):
    '''TOK_EXPRESSION : TOK_EXPRESSION_LEFT COMPARE_TYPE_EXPR TOK_EXPRESSION_RIGHT'''
    if p[2] == '!=':
        expression = ASTNode.Node(TK.TOK_COMPARE,'=',[p[1],p[3]])
        p[0] = ASTNode.Node(TK.TOK_REVERSED,'NOT'.lower(),[expression])
    else:
        p[0] = ASTNode.Node(TK.TOK_COMPARE,p[2],[p[1],p[3]])


def p_COMPARE_TYPE_EXPR(p):
    '''COMPARE_TYPE_EXPR : COMPARE_TYPE
    | LIKE'''
    p[0] = p[1]
    
    
def p_TOK_FUNCTION_EXPR(p):
    '''TOK_FUNCTION_EXPR : TOK_BEWTEEN
    | TOK_FUNCTION
    | TOK_ISNULL'''
    p[0] = p[1]
    
   
def p_TOK_FUNCTION(p):
    '''TOK_FUNCTION : VALUE_EXPR TOK_TUPLE_OBJECT'''
    p[0] = ASTNode.Node(TK.TOK_FUNCTION,p[1].get_value(),p[2].get_children())
    
       
def p_TOK_BEWTEEN(p):
    '''TOK_BEWTEEN : VALUE_EXPR BETWEEN RIGHT_VALUE_EXPR AND RIGHT_VALUE_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_FUNCTION,p[2],[p[1],p[3],p[5]])


def p_TOK_ISNULL(p):
    '''TOK_ISNULL : VALUE_EXPR IS NULL
    | VALUE_EXPR IS NOT NULL'''
    if len(p) == 4:
        p[0] = ASTNode.Node(TK.TOK_FUNCTION,'ISNULL',[p[1]])
    else:
        expression = ASTNode.Node(TK.TOK_FUNCTION,'ISNULL',[p[1]])
        p[0] = ASTNode.Node(TK.TOK_REVERSED,'NOT'.lower(),[expression])


def p_TOK_IN_EXPR(p):
    '''TOK_IN_EXPR : TOK_EXPRESSION_LEFT IN TOK_TUPLE_OBJECT'''
    p[0] = p[0] = ASTNode.Node(TK.TOK_IN,p[2],[p[1],p[3]])
    
'''==========================================table define==========================================='''


def p_TOK_CREATE_TABLE_WITH_OPTIONS(p):
    '''TOK_CREATE_TABLE : TOK_CREATE_TABLE WITH OPTION TOK_TABLE_OPTIONS'''
    p[0] = p[1]
    p[0].append_children(p[4])
    

def p_TOK_CREATE_TABLE_WITH_META(p):
    '''TOK_CREATE_TABLE : TOK_CREATE_TABLE WITH META TOK_TABLE_METAS'''
    p[0] = p[1]
    p[0].append_children(p[4])
    
    
def p_TOK_CREATE_TABLE(p):
    '''TOK_CREATE_TABLE : CREATE TABLE TOK_TABLE_NAME TOK_TABLE_COLS'''
    p[0] = ASTNode.Node(TK.TOK_CREATE_TABLE,None,[p[3],p[4]])
    p[0].get_value()
    
    
def p_TOK_META_OPTIONS(p):
    '''TOK_META_OPTIONS : TOK_OPTIONS_OBJECT'''
    p[0] = ASTNode.Node(TK.TOK_META_OPTIONS,None,[p[1]])
            
    
def p_TOK_META_DEFINE(p):
    '''TOK_META_DEF : WORD TOK_META_OPTIONS'''
    p[0] = ASTNode.Node(TK.TOK_META_DEFINE,p[1],[p[2]])


def p_TOK_METAS_DEFINE(p):
    '''TOK_METAS_DEF : TOK_META_DEF
    | TOK_META_DEF COMMA TOK_META_DEF
    | TOK_META_DEF COMMA TOK_METAS_DEF'''
    p[0] = token_list(p)
                    

def p_TOK_TABLE_METAS(p):
    '''TOK_TABLE_METAS : "(" ")"
    | "(" TOK_METAS_DEF ")"'''
    if len(p) == 3:
        p[0] = ASTNode.Node(TK.TOK_TABLE_METAS,None,None)
    else:  
        p[0] = ASTNode.Node(TK.TOK_TABLE_METAS,None,p[2])
        
        
def p_TOK_TABLE_OPTIONS(p):
    '''TOK_TABLE_OPTIONS : TOK_OPTIONS_OBJECT'''
    p[0] = ASTNode.Node(TK.TOK_TABLE_OPTIONS,None,[p[1]])


def p_TOK_TABLE_NAME(p):
    '''TOK_TABLE_NAME : VALUE_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_TABLE_NAME,None,[p[1]])


def p_TOK_TABLE_COLS(p):
    '''TOK_TABLE_COLS : "(" ")"
    | "(" TOK_COLUMNS_DEFINE ")"'''
    if len(p) == 3:
        p[0] = ASTNode.Node(TK.TOK_TABLE_COLUMNS,None,None)
    else:  
        p[0] = ASTNode.Node(TK.TOK_TABLE_COLUMNS,None,p[2])
            

def p_TOK_COLUMNS_DEFINE(p):
    '''TOK_COLUMNS_DEFINE : TOK_COLUMN_DEFINE
    | TOK_COLUMN_DEFINE COMMA TOK_COLUMN_DEFINE
    | TOK_COLUMN_DEFINE COMMA TOK_COLUMNS_DEFINE'''
    p[0] = token_list(p)


def p_COLUMN_TYPE(p):
    '''COLUMN_TYPE : WORD'''
    p[0] = ASTNode.Node(TK.TOK_CORE_TYPE,p[1],None)
 
 
def p_TOK_COLUMN_OBJECT_DEFINE(p):
    '''TOK_COLUMN_DEFINE : TOK_COLUMN_DEFINE AS TOK_TABLE_COLS'''
    p[0] = p[1]
    p[0].append_children(p[3])    
    

def p_p_TOK_COLUMN_OPTIONS(p):
    '''TOK_COLUMN_OPTIONS : TOK_OPTIONS_OBJECT'''
    p[0] = ASTNode.Node(TK.TOK_COLUMN_OPTIONS,None,[p[1]])


def p_TOK_COLUMN_DEFINE(p):
    '''TOK_COLUMN_DEFINE : WORD COLUMN_TYPE
    | WORD COLUMN_TYPE TOK_COLUMN_OPTIONS'''
    if len(p) == 3:
        p[0] = ASTNode.Node(TK.TOK_COLUMN_DEFINE,p[1],[p[2]])
    else:
        p[0] = ASTNode.Node(TK.TOK_COLUMN_DEFINE,p[1],[p[2],p[3]])     
        
      
      
                 

'''=================================query define========================================'''


def p_TOK_QUERY_WITH_ORDERBY(p):
    '''TOK_QUERY : TOK_QUERY ORDER BY TOK_ORDERBY'''
    p[0] = p[1]
    p[0].append_children(p[4])
    

def p_TOK_QUERY_WITH_EXPRESSIONS(p):
    '''TOK_QUERY : TOK_QUERY WHERE TOK_WHERE'''
    p[0] = p[1]
    p[0].append_children(p[3])

def p_TOK_QUERY_WITH_LIMITS(p):
    '''TOK_QUERY : TOK_QUERY LIMIT TOK_LIMIT'''
    p[0] = p[1]
    p[0].append_children(p[3])
        
        
def p_TOK_QUERY(p):
    '''TOK_QUERY : SELECT TOK_SELECT FROM TOK_FROM'''
    p[0] = ASTNode.Node(TK.TOK_QUERY,None,[p[2],p[4]])
    
    
def p_TOK_FROM(p):
    '''TOK_FROM : TOK_TABLE_NAME'''
    p[0] = ASTNode.Node(TK.TOK_FROM,None,[p[1]])

def p_TOK_FROM_WITH_ROUTING(p):
    '''TOK_FROM : TOK_TABLE_NAME "@" TOK_VALUE'''
    p[0] = ASTNode.Node(TK.TOK_FROM,None,[p[1],p[3]])
    
    
def p_TOK_WHRER(p):
    '''TOK_WHERE : EXPRESSION_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_WHERE,None,[p[1]])
               
        
def p_TOK_SELECT(p):
    '''TOK_SELECT : TOK_SELEXPRS'''
    p[0] = ASTNode.Node(TK.TOK_SELECT,None,p[1])        


def p_TOK_SELEXPR(p):
    '''TOK_SELEXPR : LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR AS VALUE_EXPR'''
    if len(p) == 2:
        p[0] = ASTNode.Node(TK.TOK_SELEXPR,None,[p[1]])
    else:
        p[0] = ASTNode.Node(TK.TOK_SELEXPR,None,[p[1],p[3]])

def p_TOK_SELEXPRS(p):
    '''TOK_SELEXPRS : TOK_SELEXPR
    | TOK_SELEXPR COMMA TOK_SELEXPR
    | TOK_SELEXPR COMMA TOK_SELEXPRS'''
    p[0] = token_list(p)


def p_TOK_LIMIT(p):
    '''TOK_LIMIT : LIMITS_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_LIMIT,None,p[1])
    
    
def p_LIMIT_EXPR(p):
    '''LIMIT_EXPR : NUMBER'''
    p[0] = ASTNode.Node(TK.TOK_VALUE,p[1],None)
 
 
def p_LIMITS_EXPR(p):
    '''LIMITS_EXPR : LIMIT_EXPR
    | LIMIT_EXPR COMMA LIMIT_EXPR'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1],p[3]]
        
        
def p_TOK_ORDERBY(p):
    '''TOK_ORDERBY : TOK_SORTS'''
    p[0] = ASTNode.Node(TK.TOK_ORDERBY,None,p[1])        


def p_TOK_SORTS(p):
    '''TOK_SORTS : TOK_SORT
    | TOK_SORT COMMA TOK_SORT
    | TOK_SORT COMMA TOK_SORTS'''
    p[0] = token_list(p)
   

def p_SORT_MODE(p):
    '''SORT_MODE : ASC
    | DESC'''
    p[0] = ASTNode.Node(TK.TOK_SORT_MODE,p[1],None)     
    
    
def p_TOK_SORT(p):
    '''TOK_SORT : LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR SORT_MODE'''
    if len(p) == 2: 
        p[0] = ASTNode.Node(TK.TOK_SORT,None,[p[1]])   
    else:
        p[0] = ASTNode.Node(TK.TOK_SORT,None,[p[1],p[2]])  
    
    
    
    
'''=================================Aggregations define========================================'''
        
def p_TOK_QUERY_WITH_GROUPBY(p):
    '''TOK_QUERY : TOK_QUERY GROUP BY TOK_GROUPBY'''
    p[0] = p[1]
    p[0].append_children(p[4])
            
        
def p_TOK_GROUPBY(p):
    '''TOK_GROUPBY : LEFT_VALUES_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_GROUPBY,None,p[1])    
    
    
    
'''=================================Load data define========================================'''    

def p_TOK_INSERT_INTO(p):
    '''TOK_INSERT_INTO : INSERT INTO TOK_TABLE_NAME TOK_INSERT_COLUMNS VALUES TOK_VALUE_ROW'''
    p[0] = ASTNode.Node(TK.TOK_INSERT_INTO,None,[p[3]] + [p[4]] + [p[6]])
    
      
  
def p_TOK_INSERT_COLUMNS(p):
    '''TOK_INSERT_COLUMNS : TOK_TUPLE_OBJECT'''
    p[0] = ASTNode.Node(TK.TOK_INSERT_COLUMNS,None,p[1].get_children())      
    
         
def p_TOK_INSERT_ROW(p):
    '''TOK_VALUE_ROW : "(" RIGHT_VALUES_EXPR ")" '''
    p[0] = ASTNode.Node(TK.TOK_INSERT_ROW,None,p[2])  

    
def p_INSERT_ROWS_EXPR(p):
    '''INSERT_ROWS_EXPR : TOK_VALUE_ROW
    | TOK_VALUE_ROW COMMA TOK_VALUE_ROW
    | TOK_VALUE_ROW COMMA INSERT_ROWS_EXPR'''
    p[0] = token_list(p)

 
def p_TOK_BULK_INTO(p):
    '''TOK_BULK_INTO : BULK INTO TOK_TABLE_NAME TOK_INSERT_COLUMNS VALUES INSERT_ROWS_EXPR'''
    
    rows = ASTNode.Node(TK.TOK_INSERT_ROWS,None,p[6])  
    
    p[0] = ASTNode.Node(TK.TOK_BULK_INTO,None,[p[3]] + [p[4]] + [rows])
    

def p_TOK_UPDATE(p):
    '''TOK_UPDATE : UPDATE TOK_TABLE_NAME SET TOK_SET_COLUMNS_CLAUSE WHERE TOK_WHERE'''
    p[0] = ASTNode.Node(TK.TOK_UPDATE,None,[p[2]] + [p[4]] + [p[6]])


def p_TOK_SET_COLUMNS(p):
    '''TOK_SET_COLUMNS_CLAUSE : KV_ELEMENTS_EXPR'''
    p[0] = ASTNode.Node(TK.TOK_SET_COLUMNS_CLAUSE,None,p[1])
    
    
    
def p_TOK_UPSERT_INTO(p):
    '''TOK_UPSERT_INTO : UPSERT TOK_TABLE_NAME SET TOK_SET_COLUMNS_CLAUSE WHERE TOK_WHERE'''
    p[0] = ASTNode.Node(TK.TOK_UPSERT_INTO,None,[p[2]] + [p[4]] + [p[6]])
    
    
def p_TOK_DELETE(p):
    '''TOK_DELETE : DELETE FROM TOK_TABLE_NAME WHERE TOK_WHERE'''
    p[0] = ASTNode.Node(TK.TOK_DELETE,None,[p[3]] + [p[5]])    
    
    
'''=================================show========================================'''  
    
    
def p_SHOW_TABLES(p):
    '''TOK_SHOW_TABLES : SHOW TABLES'''
    p[0] = ASTNode.Node(TK.TOK_SHOW_TABLES,None,None)   
       
       
'''=================================desc========================================'''  
def p_DESC_TABLE(p):
    '''TOK_DESC_TABLE : DESC TOK_TABLE_NAME'''
    p[0] = ASTNode.Node(TK.TOK_DESC_TABLE,None,[p[2]])               
    

'''=================================drop========================================'''  
def p_DROP_TABLE(p):
    '''TOK_DROP_TABLE : DROP TABLE TOK_TABLE_NAME'''
    p[0] = ASTNode.Node(TK.TOK_DROP_TABLE,None,[p[3]])  
    
    
        
def p_error(p):
    raise Exception("Illegal syntax")
    