'''
Created on Feb 9, 2017

@author: qs
'''

from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_object,parse_value
from ql.dsl import Query

def bucket_function(tree: Node,_size):
    bucket = {}
    bucket[tree.get_value()] = {}
    for i in range(0,tree.get_children_count()):
        if tree.get_child(i).get_type() == TK.TOK_DICT:
            bucket[tree.get_value()].update(parse_object(tree.get_child(i)))
    if _size != -1:
        bucket[tree.get_value()]['size'] = _size
    aggs = {"aggs":{}}
    field=bucket[tree.get_value()]['field']
    aggs['aggs'][field] = bucket
    return (field,aggs)


def bucket_field(tree: Node,_size):
    bucket = {}
    bucket['terms'] = {}  
    
    field = parse_value(tree)
    bucket['terms']['field'] = field
    if _size != -1:
        bucket['terms']['size'] = _size
    
    aggs = {"aggs":{}}
    aggs['aggs'][field] = bucket
    
    return (field,aggs)


def bucket(tree: Node,_size):
    if tree.get_type() == TK.TOK_FUNCTION:
        return bucket_function(tree,_size)
    else:
        return bucket_field(tree,_size)


def metrics_functions(selexpr,idx):
    alias = ''
    if hasattr(selexpr,'alias'):
        alias = selexpr.alias
    else:
        alias = '_' + str(idx) + '_'+ selexpr.selexpr.function_name
    metric = {}
    if selexpr.selexpr.function_name == 'count':
        metric['value_count'] = {}
        the_filed = selexpr.selexpr.function_parms[0] 
        if the_filed == '*':
            the_filed = '_index'
        metric['value_count'] = {'field':the_filed}
       
    else:
        if selexpr.selexpr.function_name.lower() in ('avg','min','max','sum','cardinality','stats','extended_stats'):
            metric[selexpr.selexpr.function_name] = {'field':selexpr.selexpr.function_parms[0]}
        else:
            metric[selexpr.selexpr.function_name] = {}
            for parm in selexpr.selexpr.function_parms:
                if type(parm) == dict:
                    metric[selexpr.selexpr.function_name].update(parm)
    return {alias:metric}



def get_metrics(selexprs):
    retval = {}
    idx = 0
    for e in selexprs:
        if type(e.selexpr) == Query.FunctionXpr:
            retval.update(metrics_functions(e,idx))
            idx = idx + 1
    return retval



class AggBuckets(object):    
    __slots__ = ('buckets')
    
    def __init__(self,tree: Node,_size,root=True):
        self.buckets = []
        for element in tree.get_children():
            self.buckets.append(bucket(element,_size))
    def dsl(self,_selexpr):
        (field,bucket) = self.buckets[0]
        aggs_body = bucket
        cur_aggs = aggs_body['aggs'][field]
        for i in range(1,len(self.buckets)):
            (field,bucket) = self.buckets[i]
            cur_aggs.update(bucket)
            cur_aggs = cur_aggs['aggs'][field]
        metrics = get_metrics(_selexpr)
        cur_aggs['aggs'] = metrics
        return aggs_body
    
    