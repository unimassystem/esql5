'''
Created on Jun 14, 2017

@author: qs
'''

from Api import esql

conn = esql.connect("http://10.68.23.81:5000")

c = conn.cursor();

c.execute("select * from flow_i")

print(c.total)

print(c.took)

for col in c.description:
    print(col[0])

for row in c.fetchall():
    print(row[10])
    
conn.close()