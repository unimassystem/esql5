

from ql.parse.ASTNode import Node
from ql.parse.parser import TK


def parse_tok_table_name(tree : Node):
    if tree.get_type() == TK.TOK_TABLE_NAME:
        return  parse_table_name(tree.get_child(0))
    else:
        pass


def parse_value(tree: Node) -> str:
    if tree.get_type() == TK.TOK_DOT:
        retval = parse_value(tree.get_child(0))
        retval += '.'
        retval += parse_value(tree.get_child(1))
        return retval
    elif tree.get_type() == TK.TOK_VALUE:
        return tree.get_value()
    else:
        pass


def parse_left_values(tree: Node) -> list:
    retval = []
    for e in tree:
        retval.append(parse_value(e))
    return retval
    

def parse_right_values(tree: Node):
    retval = []
    for e in tree:
        if e.get_type() in (TK.TOK_VALUE,TK.TOK_DOT):
            retval.append(parse_value(e))
        else:
            retval.append(parse_object(e))
    return retval


def parse_table_name(tree: Node):
    if tree.get_type() == TK.TOK_DOT:
        _index = parse_value(tree.get_child(0))
        _type = parse_value(tree.get_child(1))
    elif tree.get_type() == TK.TOK_VALUE:
        _index = tree.get_value()
        _type = None
    return (_index,_type)


def parse_kv(tree: Node):
    right=None
    left=None
    if tree.get_type() == TK.TOK_KEY_VALUE:
        left = parse_value(tree.get_child(0).get_child(0))
        if tree.get_child(1).get_child(0).get_type() in (TK.TOK_DICT,TK.TOK_LIST):
            right = parse_object(tree.get_child(1).get_child(0))
        else:
            right = parse_value(tree.get_child(1).get_child(0))
    else:
        pass
    return {left:right}


def parse_object(tree: Node):
    retval = None
    if tree.get_type() == TK.TOK_DICT:
        retval = {}
        for element in tree.get_children():
            retval.update(parse_kv(element))
    if tree.get_type() == TK.TOK_LIST:
        retval = []
        for element in tree.get_children():
            if element.get_type() in (TK.TOK_DICT,TK.TOK_LIST):
                retval.append(parse_object(element))
            else:
                retval.append(parse_value(element))
    return retval
