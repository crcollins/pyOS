import datetime
import sqlite3

from kernel.constants import USERDATAFILE

def convert_many(start, *args):
    if type(start) not in (list, set, tuple):
        done = [(start, ) + args]
    else:
        done = [(x, ) + args for x in start]
    return done

def build_user_data_database():
    addsql = 'INSERT INTO userdata VALUES (?, ?, ?)'
    tablesql = '''CREATE TABLE IF NOT EXISTS userdata (
                    uid TEXT,
                    gid TEXT,
                    password TEXT)'''

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    items = (("root", "root", "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1"), # pass
            ("chris", "chris", "2744ccd10c7533bd736ad890f9dd5cab2adb27b07d500b9493f29cdc420cb2e0")) # me

    with con:
        cur = con.cursor()
        cur.execute(tablesql)
        cur.executemany(addsql, items)

def get_user_data(uid):
    data = None

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM userdata WHERE uid = ?", (uid, ))
        data = cur.fetchone()
        if data:
            ## force data to be strings and not unicode
            data = tuple(str(x) if type(x) == unicode else x for x in data)
    return data

def add_user(uid, gid, password):
    addsql = 'INSERT INTO userdata VALUES (?, ?, ?)'

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute(tablesql)
        cur.executemany(addsql, items)

def delete_user(uid):
    path = convert_many(uid)
    delsql = 'DELETE FROM userdata WHERE uid = ?'

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.executemany(delsql, uid)

def get_gid(uid):
    return get_user_data(uid)[1]

def set_gid(uid, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET gid = ? WHERE uid = ?", (value, uid))

def get_password(uid):
    return get_user_data(uid)[1]

def set_password(uid, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET password = ? WHERE uid = ?", (value, uid))

def correct_password(uid, password):
    data = get_user_data(uid)
    if data is None:
        return 0
    return data[2] == password
