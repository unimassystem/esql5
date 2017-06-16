# lextab.py. This file automatically created by PLY (version 3.10). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('NOT', 'IS', 'COMMA', 'GROUP', 'QUOTE_STRING', 'DESC', 'TABLES', 'OR', 'LIKE', 'BULK', 'FROM', 'ORDER', 'NULL', 'UPSERT', 'TABLE', 'UPDATE', 'SET', 'LIMIT', 'EXPLAIN', 'WHERE', 'DELETE', 'SHOW', 'COMPARE_TYPE', 'TO', 'ASC', 'WORD', 'SELECT', 'BY', 'AS', 'INSERT', 'DROP', 'AND', 'CREATE', 'VALUES', 'WITH', 'META', 'DQUOTE_STRING', 'OPTION', 'INTO', 'BETWEEN', 'NUMBER'))
_lexreflags   = 64
_lexliterals  = '(){}@%.*[]:-^'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_WORD>[_a-zA-Z][a-zA-Z_0-9]*|[\\u4e00-\\u9fa5]+)|(?P<t_NUMBER>(\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]? \\d+)?)|(?P<t_QUOTE_STRING>\'((?<=\\\\)\\\'|[^\\\'])*\')|(?P<t_DQUOTE_STRING>"((?<=\\\\)\\"|[^\\"])*")|(?P<t_COMPARE_TYPE><>|\\!=|==|>=|<=|=>|=<|=|>|<)|(?P<t_COMMA>,)|(?P<t_END_QUERY>;)', [None, ('t_WORD', 'WORD'), ('t_NUMBER', 'NUMBER'), None, None, None, ('t_QUOTE_STRING', 'QUOTE_STRING'), None, ('t_DQUOTE_STRING', 'DQUOTE_STRING'), None, (None, 'COMPARE_TYPE'), (None, 'COMMA'), (None, 'END_QUERY')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
