from ast import Delete
import re
import psycopg2
import json

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
result = cursor.close()


conn.close()
#print(result)

