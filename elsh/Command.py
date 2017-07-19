from __future__ import unicode_literals
import sys
from pygments.token import (Keyword,
                            Comment,
                            Operator,
                            Number,
                            Literal,
                            String,
                            Error)
from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token
import os
import urllib3
from tabulate import tabulate
import json
from pygments.lexers.sql import SqlLexer


sql_completer = WordCompleter(['create', 'select', 'insert', 'drop',
                               'delete', 'from', 'where', 'table',
                               'bulk','update','limit','group','by',
                               'index.number_of_shards','index.number_of_replicas',
                               'index.flush_inteval','moving_avg','date_range','date_histogram'], ignore_case=True)


def do_esql(database,statement):
    url = database.host.rstrip() + database.url
    http = urllib3.PoolManager()
    try:
        res = http.request('POST', url, fields = {"sql":statement})
    except Exception as e:
        print(str(e))
        return
    if res.status != 200:
        print(res.data.decode('utf-8'))
    else:
        gb = json.loads(res.data.decode('utf-8'))
        table = gb['rows']
        headers = gb['cols']
        print(tabulate(table, headers, tablefmt="grid",disable_numparse=True))
        if 'total' not in gb:
            gb['total'] = 0
        if 'took' not in gb:
            gb['took'] = 0
        print('%d rows affected (%.3f seconds) '%(gb['total'],gb['took']/1000))
 
        
class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
        Keyword: 'bold #4b95a3',
        Comment: '#757265',
        Operator: '#e83131',
        Number: '#be61ff',
        Literal: '#ae81ff',
        String: '#f4a33d',
        Error: '#ff3300',
    }
    styles.update(DefaultStyle.styles)


class Database():
    
    __slots__ = ('host','url','user','passwd')
    def __init__(self,host):
        self.url = '/esql'
        self.host = host
        self.user = ''
        self.passwd = ''
    
    def set_host(self,host):
        self.url = host
        
    def set_urer(self,user,passwd):
        self.user = user
        self.passwd = passwd


def do_config(args,database):
    config = args.split(' ')
    if config[0] == 'connect':
        database.host = config[1]

def main(database):
    history = InMemoryHistory()
    input_line = ''
    newline=True
    while True:
        try:
            if newline:
                text = prompt('esql> ',lexer = SqlLexer, completer=sql_completer,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
            else:
                text = prompt('...> ', lexer = SqlLexer,completer=sql_completer,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
            
            input_line += os.linesep + text.rstrip()
            if input_line.endswith(';'):
                if input_line[1] == '\\':
                    do_config(input_line[2:len(input_line)-1],database)
                else:
                    do_esql(database,input_line[:len(input_line)-1])
                newline = True
                input_line = ''
            else:
                newline = False
            
        except EOFError:
            break  # Control-D pressed.
    print('GoodBye!')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        db = 'http://127.0.0.1:5000'
    else:
        db = sys.argv[1]

    print('Ctrl + D Quit Esql shell')
    main(Database(db))
    
    
    