import sqlite3
import shutil
import os

connection_db = sqlite3.connect('database/persons.db')

sql_query = "DELETE from Persons;"

person_iterable = connection_db.cursor().execute(sql_query)
connection_db.commit()
start = 0
for person in person_iterable:
   print(person[start])

connection_db.close()

shutil.rmtree('images')
os.makedirs('images')

print("Successfully Deleted")