'''
Created on Jun 14, 2017

@author: qs
'''
import urllib3
import json

def connect(db_host):
    return connector(db_host)
    
class connector():
    def __init__(self,db_host):
        self._db_host = db_host
    def cursor(self):
        return cursor(self._db_host) 
    
    def close(self):
        pass
    
class cursor():
    __slots__ = ('_db_host','_res','description','total','took')
    
    def __init__(self,db_host):
        print("new cursor")
        self._db_host = db_host

    def execute(self,statement):
        http = urllib3.PoolManager()
        url = self._db_host + '/esql'
        try:
            res = http.request('POST', url, fields = {"sql":statement})
        except Exception:
            raise Exception("Connection refused")
        if res.status != 200:
            raise Exception(res.data.decode('utf-8'))
        self._res = json.loads(res.data.decode('utf-8'))
        self.description = tuple(tuple((item,None,None,None,None,None,None)) for item in self._res['cols'])
        if 'total' in self._res.keys():
            self.total = self._res['total']
        if 'took' in self._res.keys():
            self.took = self._res['took']
        
    def fetchall(self):
        res = []
        for row in self._res['rows']:
            res.append(tuple(item for item in row))
        return res
    
    
