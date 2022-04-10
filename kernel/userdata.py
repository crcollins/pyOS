import sqlite3

from kernel.constants import USERDATAFILE
from kernel.utils import convert_many

def build_user_data_database():
    addsql = 'INSERT INTO userdata VALUES (?, ?, ?, ?, ?, ?)'
    tablesql = '''CREATE TABLE IF NOT EXISTS userdata (
                    username TEXT,
                    groupname TEXT,
                    info TEXT,
                    homedir TEXT,
                    shell TEXT,
                    password TEXT)'''

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    root = ("root", "root", 'Root', '/', "/programs/interpreter",
    "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1") # pass
    chris = ("chris", "chris", 'Chris', '/', "/programs/interpreter",
    "2744ccd10c7533bd736ad890f9dd5cab2adb27b07d500b9493f29cdc420cb2e0") # me
    with con:
        cur = con.cursor()
        cur.execute(tablesql)
        if get_user_data("chris") is None:
            cur.execute(addsql, chris)
        if get_user_data("root") is None:
            cur.execute(addsql, root)

def get_user_data(user):
    data = None

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ?", (user, ))
        data = cur.fetchone()
        if data:
            ## force data to be strings and not unicode
            data = tuple(str(x) if type(x) == str else x for x in data)
    return data

def get_all_user_data():
    data = None

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM userdata")
        data = cur.fetchall()
        if data:
            ## force data to be strings and not unicode
            data = [tuple(str(x) if type(x) == str else x for x in row) for row in data]
    return data

#######################################

def add_user(user, group, info, homedir, shell, password):
    addsql = 'INSERT INTO userdata VALUES (?, ?, ?, ?, ?, ?)'

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute(addsql, (user, group, info, homedir, shell, password))

def delete_user(user):
    user = convert_many(user)
    delsql = 'DELETE FROM userdata WHERE username = ?'

    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.executemany(delsql, user)

def change_user(user, value):
    pass

#######################################

def get_group(user):
    return get_user_data(user)[1]

def set_group(user, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET groupname = ? WHERE username = ?", (value, user))

def get_info(user):
    return get_user_data(user)[2]

def set_info(user, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET info = ? WHERE username = ?", (value, user))

def get_homedir(user):
    return get_user_data(user)[3]

def set_homedir(user, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET homedir = ? WHERE username = ?", (value, user))

def get_shell(user):
    return get_user_data(user)[4]

def set_shell(user, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET shell = ? WHERE username = ?", (value, user))

def get_password(user):
    return get_user_data(user)[5]

def set_password(user, value):
    con = sqlite3.connect(USERDATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE userdata SET password = ? WHERE username = ?", (value, user))

#######################################

def correct_password(user, password):
    try:
        return get_password(user) == password
    except TypeError:
        return 0
