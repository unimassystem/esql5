'''
Created on Apr 19, 2017

@author: qs
'''

from App.utils import http_response_error,http_response_succes,http_response_nor
import yaml
import os
from elasticsearch import Elasticsearch
from ql.parse import lexer
from ql.parse import parser
from ply.lex import  lex
from ply.yacc import yacc
from ql.dsl.Query import Query
from ql.dsl.Response import response_hits,response_nor,response_cat,response_mappings,response_bulk
from elasticsearch import ElasticsearchException
from ql.parse.parser import TK
from ql.dsl.Create import Create
from ql.dsl.Describe import Describe
from ql.dsl.Insert import Insert,Bulk
from ql.dsl.Update import Update,Upsert
from ql.dsl.Delete import Delete
from ql.dsl.Drop import Drop
from ql.dsl.Explain import Explain
import time


ESQL_HOME = os.path.realpath(os.path.join(__file__, '..', '..'))


class Esql():
    def __init__(self):
        conf_file = open(os.path.join(ESQL_HOME,'conf','esql.yml'), 'r')
        app_conf = yaml.load(conf_file)
        conf_file.close()
        self.es_hosts = app_conf['elastic'].get('hosts')
        self.es_handler = Elasticsearch(self.es_hosts)
        self.lexer = lex(module=lexer,optimize=True,debug=False)
        self.parser = yacc(debug=False,module=parser)
    
    
    def get_host_url(self):
        return "http://" + self.es_hosts[0]['host'] + ":" + str(self.es_hosts[0]['port'])
    
    
    
    def _exec_query(self,ast):
    
        try:
            stmt = Query(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        
        try:
            hits = self.es_handler.search(index=stmt._index, doc_type = stmt._type, body = stmt.dsl(), request_timeout=100)
        except ElasticsearchException as e:
            return http_response_error(str(e))
        try:
            mappings = self.es_handler.indices.get_mapping(index=stmt._index, doc_type = stmt._type)
        except ElasticsearchException as e:
            return http_response_error(str(e))
        selecols = stmt.dsl()['_source']
        stmt_res = None
        try:
            stmt_res = response_hits(hits,mappings,selecols)
        except Exception as e:
            return http_response_nor(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_create_table(self,ast):
    
        start_time = time.time()
        try:
            stmt = Create(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            res = self.es_handler.indices.create(index=stmt._index,body = stmt._options,request_timeout=100,ignore= 400)
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.indices.put_mapping(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), request_timeout=100)
        except ElasticsearchException as e:
            return http_response_nor(str(e))
        
        stmt_res = None
        
        end_time = time.time()
        
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_show_tables(self,ast):
    
        start_time = time.time()

        try:
            res = self.es_handler.cat.indices(v=True,bytes='b',h=['index','status','pri','rep','docs.count','store.size'])
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = res
   
        end_time = time.time()
        
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_cat(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
        
    
    def _exec_desc_table(self,ast):
        start_time = time.time()
        try:
            stmt = Describe(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            res = self.es_handler.indices.get_mapping(index = stmt._index, doc_type = stmt._type)
        except ElasticsearchException as e:
            return http_response_error(e.error)

        stmt_res = None
        
        end_time = time.time()
        
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_mappings(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_drop_table(self,ast):
        start_time = time.time()
        try:
            stmt = Drop(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            res = self.es_handler.indices.delete(index = stmt._index)
        except ElasticsearchException as e:
            return http_response_error(e.error)
        
        stmt_res = None
        
        end_time = time.time()
        
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    def _exec_insert_into(self,ast):
        start_time = time.time()
        try:
            stmt = Insert(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            parms = stmt.metas
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.index(index = stmt._index,doc_type =  stmt._type, body = stmt.dsl(),**parms)
            
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = None
        end_time = time.time()
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_bulk_into(self,ast):

        try:
            stmt = Bulk(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.bulk(index = stmt._index,doc_type = stmt._type, body = stmt.dsl())
            
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = None

        try:
            stmt_res = response_bulk(res)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    
    def _exec_update(self,ast):
        start_time = time.time()
        try:
            stmt = Update(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.update(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), **stmt.conditions)
            
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = None

        end_time = time.time()
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_upsert(self,ast):
        start_time = time.time()
        try:
            stmt = Upsert(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.update(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), **stmt.conditions)
            
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = None

        end_time = time.time()
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
        
    def _exec_delete(self,ast):
        start_time = time.time()
        try:
            stmt = Delete(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        try:
            if stmt._type == None:
                stmt._type = 'base'
            res = self.es_handler.delete(index = stmt._index, doc_type = stmt._type, **stmt.conditions)
            
        except ElasticsearchException as e:
            return http_response_error(str(e))
        
        stmt_res = None

        end_time = time.time()
        took = int((end_time - start_time)*1000)
        try:
            stmt_res = response_nor(res,took)
        except Exception as e:
            return http_response_error(str(e))
        return http_response_succes(stmt_res)
    
    
    def _exec_explain(self,ast):
        try:
            stmt = Explain(ast)
        except Exception:
            return http_response_error('Parse statement to dsl error!')
        return http_response_nor(stmt.dsl(),202)
    
    
    def exec_statement(self,sql):
        ast = None
        try:
            ast = self.parser.parse(lexer=self.lexer.clone(),debug=False,input=sql)
        except Exception as e:
            return http_response_error(str(e))

        if ast == None:
            return http_response_error('parse statement error')
        
        if ast.get_type() == TK.TOK_QUERY:
            return self._exec_query(ast)
        elif ast.get_type() == TK.TOK_CREATE_TABLE:
            return self._exec_create_table(ast)
        elif ast.get_type() == TK.TOK_SHOW_TABLES:
            return self._exec_show_tables(ast)
        elif ast.get_type() == TK.TOK_DESC_TABLE:
            return self._exec_desc_table(ast)
        elif ast.get_type() == TK.TOK_INSERT_INTO:
            return self._exec_insert_into(ast)
        elif ast.get_type() == TK.TOK_BULK_INTO:
            return self._exec_bulk_into(ast)
        elif ast.get_type() == TK.TOK_UPDATE:
            return self._exec_update(ast)
        elif ast.get_type() == TK.TOK_UPSERT_INTO:
            return self._exec_upsert(ast)   
        elif ast.get_type() == TK.TOK_DELETE:
            return self._exec_delete(ast)
        elif ast.get_type() == TK.TOK_DROP_TABLE:
            return self._exec_drop_table(ast)    
        elif ast.get_type() == TK.TOK_EXPLAIN:
            return self._exec_explain(ast)
        else:
            return http_response_error('Syntax not supported!')
        
        
        
