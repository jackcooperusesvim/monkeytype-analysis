import eda 
import config
import sqlite3


data = eda.import_filt()

conn = sqlite3.connect(config.DATABASE_FILEPATH())

cur = conn.cursor()

with open("queries/init_db.sql","r") as file:
    cur.execute(file.read())
    conn.commit()

