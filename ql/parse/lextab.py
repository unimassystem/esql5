# lextab.py. This file automatically created by PLY (version 3.9). Don't edit!
_tabversion   = '3.8'
_lextokens    = set(('INTO', 'FROM', 'NUMBER', 'NOT', 'ORDER', 'BY', 'WORD', 'IS', 'UPSERT', 'CREATE', 'NULL', 'INSERT', 'BETWEEN', 'BULK', 'META', 'TO', 'VALUES', 'GROUP', 'DESC', 'WHERE', 'COMMA', 'LIMIT', 'WITH', 'TABLE', 'OPTION', 'COMPARE_TYPE', 'ASC', 'AS', 'LIKE', 'EXPLAIN', 'OR', 'DELETE', 'SELECT', 'UPDATE', 'DQUOTE_STRING', 'QUOTE_STRING', 'SET', 'AND', 'END_QUERY'))
_lexreflags   = 0
_lexliterals  = '(){}@%.*[]:-^'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_WORD>[_a-zA-Z][a-zA-Z_0-9]*|[\\u4e00-\\u9fa5]+)|(?P<t_NUMBER>(\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]? \\d+)?)|(?P<t_QUOTE_STRING>\'((?<=\\\\)\\\'|[^\\\'])*\')|(?P<t_DQUOTE_STRING>"((?<=\\\\)\\"|[^\\"])*")|(?P<t_COMPARE_TYPE><>|\\!=|==|>=|<=|=>|=<|=|>|<)|(?P<t_COMMA>,)|(?P<t_END_QUERY>;)', [None, ('t_WORD', 'WORD'), ('t_NUMBER', 'NUMBER'), None, None, None, ('t_QUOTE_STRING', 'QUOTE_STRING'), None, ('t_DQUOTE_STRING', 'DQUOTE_STRING'), None, (None, 'COMPARE_TYPE'), (None, 'COMMA'), (None, 'END_QUERY')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
