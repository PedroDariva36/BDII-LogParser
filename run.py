
import psycopg2
import json

# DEFS

#files

METAFILE = "metadado.json"
LOGFILE = "entradaLog(1)"
OUTFILENAME = "out.json"

#db
HOST = "localhost"
DATABASE = "postgres"
USER = "postgres"
PASSWORD = "postgres"
TABLENAME = "exemplo"

def connUp():
    return psycopg2.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD) 

def getMetadata():
    file = open(METAFILE)
    metadata = json.load(file)
    return metadata["INITIAL"]



# RESET
conn = connUp()
cursor = conn.cursor()
cursor.execute("delete from " + TABLENAME + " where 1=1")
conn.commit()


a = getMetadata()
keys = a.keys()
rn = 0
for k in keys:
    rn = len(a[k])
    break


for i in range(rn):
    s = 'insert into ' + TABLENAME + ' values ({},'.format(i+1)
    for k in keys:
        s = s + "{},".format(a[k][i])
    s = s[:-1] + ");"
    print(s)
    cursor.execute(s)
conn.commit()
print()
# PARSE LOG

redo = set()
undo = set()
general = list()


log = open(LOGFILE)
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
    cursor.execute("update " + TABLENAME + " set "+ i[2] + " = {} where id = {};".format(i[4],i[1]))
    conn.commit()

general.reverse()

for i in general:
    if(i != [] and i[0] in undo):
        cursor.execute("update " + TABLENAME + " set "+ i[2] + " = {} where id = {};".format(i[3],i[1]))
        conn.commit()


for i in redo:
    print("Transação " + i + " realizou REDO")

for i in undo:
    print("Transação " + i + " realizou UNDO")



cursor.execute("Select * from " + TABLENAME + ";")
conn.commit()

list = {}
indk = []
for k in keys:
    indk.append(str(k))
    list[str(k)] = []

all = cursor.fetchall()
for l in all:
    for i in range(len(indk)):
        list[indk[i]].append(l[i+1])

final = {"FINAL": list}

json_object = json.dumps(final, indent=2)
with open(OUTFILENAME, "w") as outfile:
    outfile.write(json_object)

print("Resultado final está no arquivo " + OUTFILENAME)

# END
cursor.close()
conn.close()


