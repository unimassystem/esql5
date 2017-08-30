'''
Created on Dec 15, 2016

@author: qs
'''


reserved = {
    'select': 'SELECT',
    'insert': 'INSERT',
    'bulk': 'BULK',
    'upsert': 'UPSERT',
    'update': 'UPDATE',
    'delete': 'DELETE',
    'create': 'CREATE',
    'set': 'SET',
    'from': 'FROM',
    'to': 'TO',
    'is': 'IS',
    'null': 'NULL',
    'where': 'WHERE',
    'into': 'INTO',
    'values': 'VALUES',
    'drop': 'DROP',
    'and': 'AND',
    'or': 'OR',
    'in': 'IN',
    'as': 'AS',
    'with': 'WITH',
    'meta': 'META',
    'option': 'OPTION',
    'like': 'LIKE',
    'limit': 'LIMIT',
    'between': 'BETWEEN',
    'not': 'NOT',
    'table': 'TABLE',
    'asc': 'ASC',
    'desc': 'DESC',
    'order': 'ORDER',
    'group': 'GROUP',
    'by': 'BY',
    'explain': 'EXPLAIN',
    'show': 'SHOW',
    'tables': 'TABLES',
}


tokens = (
    'COMPARE_TYPE',
    'WORD',
    'NUMBER',
    'COMMA',
    'QUOTE_STRING',
    'DQUOTE_STRING'
) + tuple(set(reserved.values()))

literals = '(){}@%.*[]:-^'
t_COMPARE_TYPE = '<>|\!=|==|>=|<=|=>|=<|=|>|<'
t_END_QUERY = ';'
t_COMMA = ','
t_ignore = ' \t\n'


def t_WORD(t):
    r'[_a-zA-Z][a-zA-Z_0-9]*|[\u4e00-\u9fa5]+'
    t.type = reserved.get(t.value.lower(),'WORD')
    return t


def t_NUMBER(t):
    r'(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_QUOTE_STRING(t):
    r"'((?<=\\)\'|[^\'])*'"
    t.value = t.value[1:-1]
    return t


def t_DQUOTE_STRING(t):
    r'"((?<=\\)\"|[^\"])*"'
    return t


def t_error(t):
    raise Exception("Illegal character '%s'", t.value[0])
    t.lexer.skip(1)
    
    
    
    