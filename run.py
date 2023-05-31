import re
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres")

cursor = conn.cursor()

cursor.execute('select * from public.exemplo;')
result = cursor.fetchall()
print(result)

