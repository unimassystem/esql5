'''
Created on Dec 23, 2016

@author: qs
'''
# -*- coding: utf-8 -*- 




from ql.parse import lexer
from ql.parse import parser
from ply.lex import  lex
from ply.yacc import yacc
from ql.parse.parser import TK

from ql.dsl.Explain import Explain
from ql.dsl.Insert import Insert,Bulk
from ql.dsl.Update import Update,Upsert
from ql.dsl.Delete import Delete
from ql.dsl.Query import Query
from ql.dsl.Response import response_hits
from ql.dsl.Create import Create
from ql.dsl.Describe import Describe
import sys
import json
from elasticsearch import Elasticsearch



def exec_query(stmt):

    my_lexer=lex(module=lexer,optimize=True,debug=True)
       
    my_parser=yacc(debug=True,module=parser)
    
    val = my_parser.parse(lexer=my_lexer.clone(),debug=False,input=sql)

    es = Elasticsearch([{'host':"10.68.23.81","port":9201}])
    
    
    val.debug()
    
    if val.get_type() == TK.TOK_QUERY:
        
        query = Query(val)
        
        print(query.dsl())
        
        print(query._index,query._type)
        
        res = es.search(index=query._index, doc_type = query._type, body=query.dsl(), request_timeout=100)
      
        stmt_res = response_hits(res)
      
        print(json.dumps(stmt_res,indent=4))
        
    elif val.get_type() == TK.TOK_CREATE_TABLE:
        
        stmt = Create(val)
        
        res = es.indices.create(index=stmt._index,body = stmt._options,request_timeout=100,ignore= 400)
    
        res = es.indices.put_mapping(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), request_timeout=100)
    
        print(json.dumps(res,indent=4))
        
    elif val.get_type() == TK.TOK_INSERT_INTO:
        
#         val.debug()
        
        stmt = Insert(val)
        
        parms = stmt.metas
        
        res = es.index(index = stmt._index,doc_type =  stmt._type, body = stmt.dsl(),**parms)
        
        print(json.dumps(res,indent=4))
        
    elif val.get_type() == TK.TOK_BULK_INTO:
        
#         val.debug()
        
        
        stmt = Bulk(val)
        
        res = es.bulk(index = stmt._index,doc_type = stmt._type, body = stmt.dsl())
        
        print(json.dumps(res,indent=4))
        
    
    elif val.get_type() == TK.TOK_UPDATE:
        
        val.debug()
        
        stmt = Update(val)
        
        print(json.dumps(stmt.dsl(),indent=4))
        
        res = es.update(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), **stmt.conditions)
        
        
        print(json.dumps(res,indent=4))
    
    
    elif val.get_type() == TK.TOK_UPSERT_INTO:
        
        val.debug()
        
        stmt = Upsert(val)
        
        print(json.dumps(stmt.dsl(),indent=4))
        
        res = es.update(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), **stmt.conditions)
        
        
        print(json.dumps(res,indent=4))
    
    
    elif val.get_type() == TK.TOK_DELETE:
        
        val.debug()
        
        stmt = Delete(val)
        
        res = es.delete(index = stmt._index, doc_type = stmt._type, **stmt.conditions,ignore= 404)

        print(json.dumps(res,indent=4))
        
        
    elif val.get_type() == TK.TOK_EXPLAIN:
        stmt = Explain(val)
        print(stmt.curl_str)
        print(json.dumps(stmt.dsl(),indent=4))
    
    elif val.get_type() == TK.TOK_DESC_TABLE:
        
        stmt = Describe(val)
        
        
        res = es.indices.get_mapping(index = stmt._index,doc_type=stmt._type)
        
        print(res)
        
        
    else:
        res = es.cat.indices(index = 'qs_test*', v=True)
        val.debug()
        print(res)

        
        
        
        


if __name__ == "__main__":

    if len(sys.argv) < 2:
        sqls = [

#         '''create table qs_test03.ccx (
#             name string (analyzer = ik),
#             timestamp date,
#             age long
#         ) with option (
#             index.number_of_shards=10,
#             index.number_of_replicas = 1,
#             index.flush_inteval='10s'
#         )''',
#         '''show tables''',
#         '''desc flow_i'''
#          
#         '''create table my_tb.ccx (
#             a string (index=no),
#             c object as (
#                 raw string (index=not_analyzed,doc_values=false),
#                 obj object as (
#                     ddd string (index=no)
#                 )
#             )
#         ) with meta (
#             _parent (type='people'),
#             _source (includes = [a,'*c'])
#         ) with option (
#             index.number_of_shards=10,
#             index.number_of_replicas = 1,
#             index.flush_inteval='10s'
#         );''',
   
#         '''select * from _all''', 
         
#         '''select count(*) as c,count(*) as cc ,sum(dd) as dd,moving_avg({buckets_path=c,window=30,model=simple}), moving_avg({buckets_path=dd,window=30,model=simple})  
#         from my_index02 
#         group by name,date_histogram({field=ts,interval='1h'});''',
#          
#         '''select count(*) from my_index02 group by date_range({field=ts,ranges=[{to='now-10M/M',from=now},{to='now',from='now-10M/M'}]});''',
#        
#         '''insert into my_index.base (_id,_routing,name,age,address,message) values (200,200,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms001','sms002'])''',
# #          
#         '''bulk into my_index_occ.base(_id,name,age,address,message) values 
#             (1,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']),
#             (2,'zhangsan',25,{address='zhejiang',postCode='330010'},['sms:001','sms:002'])''', 
#  
#          
#         '''update my_index_occ.base set name = 'lisi' ,age = 30,address={address='shanghai',postCode='3300100009'} where _id = 1''',
#             
#          '''upsert  my_index_occ.base set name1 = 'lisi' ,age1 = 30,address1={address='shanghai',postCode='3300100009'} where _id = 1''',
#            
#         '''delete from my_index_occ where _id = 1;''',
#         
#                        
#         '''explain select count(*) as c,count(*) as cc ,sum(dd) as dd,moving_avg({buckets_path=c,window=30,model=simple}), moving_avg({buckets_path=dd,window=30,model=simple})  
#         from my_index02 
#         group by name,date_histogram({field=ts,interval='1h'});''',
#         
        '''select * from "config_log-'23'".base where app_name in ("login",'policy') and app_id > 1001 and app_ii = "2001"''',
        
        
        ]

        for sql in sqls:
            exec_query(sql)
                
    else: 
        sql = sys.argv[1]
        exec_query(sql)
        
        
