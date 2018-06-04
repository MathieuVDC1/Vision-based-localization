#!/usr/bin/python

import sys
import sqlite3 as sq
import pickle

conn = sq.connect('database.sqlite')
c = conn.cursor()


def main():
    conn = sq.connect('database.sqlite')
    c = conn.cursor()

    for i in range (1, len(sys.argv)):
        arg = sys.argv[i].lower()
        if arg ==   "drop":
            print("Dropping table 'data'")
            c.execute("DROP TABLE data")
            conn.commit()
        elif arg ==   "init":
            print("Creating table 'data'")
            createTable(c)
            conn.commit()
        elif arg == "clear":
            print("Clearing table 'data'")
            c.execute("DELETE FROM data")
            conn.commit()
        elif arg == "fill":
            print("Filling table 'data'")
            fill(c)
            conn.commit()
        elif arg == "query":
            for row in c.execute(sys.argv[i+1]):
                printRow(row)
    
    conn.close()
    
def printRow(row):
    for field in row:
        if field == "":
            print(row)
            return

    lines = pickle.loads(row[2])
    streets = pickle.loads(row[3])
    signs = pickle.loads(row[4])
    features = pickle.loads(row[5])

    print("%s => %s\t" % (row[1], row[0]), lines, "\t", streets, "\t", signs, "\t", features)

def fill(cursor):
    data = [5, 6, 7, 8, [9, 10, 11]]
    s = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    for i in range(0, 100000):
        cursor.execute("INSERT INTO data (name, video, lines, streets, signs, features) VALUES (?, 'video1', ?, ?, ?, ?)", ['frame' + str(i), s, s, s, s])

def createTable(cursor):
    query = '''CREATE TABLE data
                    (name VARCHAR(50) UNIQUE, video VARCHAR(50), lines BLOB,
                     streets BLOB, signs BLOB, features BLOB)'''
    cursor.execute(query)

    query = "CREATE INDEX data_index ON data (name)"
    cursor.execute(query)

def insertRow(name, video, lines, streets, signs, features):
    lines = pickle.dumps(lines, pickle.HIGHEST_PROTOCOL)
    streets = pickle.dumps(streets, pickle.HIGHEST_PROTOCOL)
    signs = pickle.dumps(signs, pickle.HIGHEST_PROTOCOL)
    features = pickle.dumps(features, pickle.HIGHEST_PROTOCOL)
    c.execute("INSERT INTO data (name, video, lines, streets, signs, features) VALUES (?, 'video1', ?, ?, ?, ?)", ['frame' + str(i), s, s, s, s])

def updateRow(name, fieldname, object):
    object = pickle.dumps(object, pickle.HIGHEST_PROTOCOL)
    c.execute("UPDATE data SET ? = ? WHERE name = ?", [fieldname, object, name])

if __name__ == "__main__":
    main()