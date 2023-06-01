from audioop import reverse
import re
import psycopg2
import json

# DEFS

def connUp():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")
    return conn

def getMetadata():
    file = open("metadado.json")
    metadata = json.load(file)
    return metadata["INITIAL"]






# RESET
conn = connUp()
cursor = conn.cursor()
cursor.execute("delete from exemplo where 1=1")
conn.commit()


a = getMetadata()
for i in range(len(a["A"])):
    s = 'insert into public.exemplo values ({},{},{});'.format(i+1, a["A"][i], a["B"][i])
    print(s)
    cursor.execute(s)
conn.commit()

# PARSE LOG

redo = set()
undo = set()
general = list()


log = open("entradaLog(1)")
lines = log.readlines()
for l in lines:
    l = l.replace('<', '')
    l = l.replace('>','')
    l = l.replace('\n', '')
    l = l.replace(',',' ')
    #print(l)
    list = l.split()
    #print(list)
    if(len(list) == 2):
        if (list[0] == "start"):
            redo.add(list[1])
        else:
            undo.add(list[1])
            redo.remove(list[1])
    else:
        general.append(list)
    
for i in general:
    if(i == []):
        continue
    cursor.execute("update exemplo set "+ i[2] + " = {} where id = {}".format(i[4],i[1]))
    conn.commit()

general.reverse()

for i in general:
    if(i != [] and i[0] in undo):
        cursor.execute("update exemplo set "+ i[2] + " = {} where id = {}".format(i[3],i[1]))
        conn.commit()

for i in redo:
    print("Transação " + i + " realizou REDO")

for i in undo:
    print("Transação " + i + " realizou UNDO")



# END
cursor.close()
conn.close()


