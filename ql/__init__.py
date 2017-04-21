from ply.lex import lex
from ply.yacc import yacc

from ql.parse import lexer, parser
from ql.dsl.Query import Query

__debug = False
__lexer = None
__parser = None


def init(optimize, debug):
    """ Init parser
    """
    global __debug, __lexer, __parser
    __debug = debug
    __lexer = lex(module=lexer, optimize=optimize, debug=debug)
    __parser = yacc(debug=debug, module=parser)


def parse(sql):
    ast = __parser.parse(input=sql, lexer=__lexer.clone(), debug=__debug)
    if not ast:
        return None
    ast.debug()
    return Query(ast)
