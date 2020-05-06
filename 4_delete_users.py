import sqlite3
import shutil
import os

connection_db = sqlite3.connect('database/persons.db')

cursor = connection_db.cursor().execute("DELETE from Persons;")
connection_db.commit()

for row in cursor:
   print(row[0])

connection_db.close()

shutil.rmtree('images')
os.makedirs('images')

print("Successfully Deleted")