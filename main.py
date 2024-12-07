from datetime import datetime
import sqlite3

con = sqlite3.connect("klass1.db")
cur = con.cursor()
cur.execute("CREATE TABLE if not exists lesson(weekday, name, start, end)")

cur.execute("""
    INSERT INTO lesson VALUES(0 ,"тест", "8:00", "8:40")
""")
con.commit()

cur.execute("""
    DELETE FROM lesson WHERE start = "8:00" and weekday=0
""")
con.commit()
res = cur.execute("SELECT name, start, end FROM lesson")
print(res.fetchall())

while True:
    inp = input("stupid asking line!!!!!: ")
    if inp == "schedule":
        if input() == 'понедельник':
            res = cur.execute('SELECT name, start, end FROM lesson WHERE weekday=0')

        res = cur.execute("SELECT name, start, end FROM lesson")
        print(res.fetchall())



