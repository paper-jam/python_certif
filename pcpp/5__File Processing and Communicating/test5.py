import sqlite3
import os
import sys


path_for_db = os.path.realpath(os.path.dirname(__file__))
db_file = os.path.join(path_for_db, "tasks.db")


def find_task(id, name):
    if id < 1 or not name:
        print("both id and name must be filled in")
        return

    c = conn.cursor()

    c.execute("SELECT * FROM tasks where id=? and name=?", (id, name))
    row = c.fetchone()
    print(row)
    return


def show_task():
    c = conn.cursor()
    for row in c.execute("SELECT * FROM tasks"):
        print(row)


os.chdir("C:\\Users\\Francis\\Google Drive\\projet\\MemoAndShortkey\\Python\\pcpp\\5__File Processing and Communicating")
conn = sqlite3.connect(db_file)


# conn.execute('''CREATE TABLE tasks (id INTEGER PRIMARY KEY,name TEXT NOT NULL,priority INTEGER NOT NULL);''')


# execute many use a list of tuples
# tasks = [
#     ('My first task', 1),
#     ('My second task', 5),
#     ('My third task', 10),
# ]
# conn.executemany('INSERT INTO tasks (name, priority) VALUES (?,?)', tasks)
# conn.commit()

show_task()
find_task(2, "My second task")

conn.close()
