'''
Created on Apr 21, 2017

@author: qs
'''

from flask import Flask
from flask import request
from App.utils import http_response_error
from App.esql import Esql
from flask import redirect


esql = Esql()
app  = Flask(__name__,static_folder='../head')

def request_sql():
    if request.method == 'GET':
        return request.args.get('sql')
    else:
        return request.form.get('sql')



@app.route('/')
def home():
    url = esql.get_host_url()
    return redirect('head/index.html?base_uri=' + url)


@app.route('/esql',methods=('GET','POST'))
def app_esql():
    sql = request_sql()
    
    if sql == None:
        return http_response_error('Statement not found!')
    
    return esql.exec_statement(sql)
     
    
if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000)
    
    