import datetime
import sqlite3

from kernel.constants import METADATAFILE

def convert_many(start, *args):
    if type(start) not in (list, set, tuple):
        done = [(start, ) + args]
    else:
        done = [(x, ) + args for x in start]
    return done

def build_meta_data_database(fsmatches):
    now = datetime.datetime.now()

    delsql = 'DELETE FROM metadata WHERE path = ?'
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)'
    tablesql = '''CREATE TABLE IF NOT EXISTS metadata (
                    path TEXT,
                    owner TEXT,
                    permission TEXT,
                    created TIMESTAMP,
                    accessed TIMESTAMP,
                    modified TIMESTAMP)'''

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT path FROM metadata")
            fsmatches = set(fsmatches)
            dbmatches = set(x[0] for x in cur.fetchall())

            for x in fsmatches.difference(dbmatches):
                cur.execute(addsql, ((x, "root", "rwxrwxrwx", now, now, now)))
            for x in dbmatches.difference(fsmatches):
                cur.execute(delsql, (x, ))

    except:
        items = ((x, "root", "rwxrwxrwx", now, now, now) for x in fsmatches)

        with con:
            cur = con.cursor()
            cur.execute(tablesql)
            cur.executemany(addsql, items)

def get_meta_data(path):
    data = None

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM metadata WHERE path = ?", (path, ))
        data = cur.fetchone()
        if data:
            ## force data to be strings and not unicode
            data = tuple(str(x) if type(x) == unicode else x for x in data)
    return data

def get_all_meta_data(path='/'):
    data = None

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM metadata WHERE path LIKE ?", (path+'%', ))
        data = cur.fetchall()
        if data:
            ## force data to be strings and not unicode
            data = [tuple(str(x) if type(x) == unicode else x for x in row) for row in data]
    return data

def add_path(path, owner, permission):
    now = datetime.datetime.now()

    validate_permission(permission)
    validate_owner(owner)

    data = convert_many(path, owner, permission, now, now, now)

    addsql = 'INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)'

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.executemany(addsql, data)

def copy_path(src, dst):
    now = datetime.datetime.now()

    src = convert_many(src)
    dst = convert_many(dst)
    assert len(src) == len(dst)

    selsql = 'SELECT owner,permission FROM metadata WHERE path = ?'
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)'

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        temp = []
        for x in src:
            cur.execute(selsql, x)
            temp.append(cur.fetchone())

        # fix for ignored files
        zipped = ((x, y) for (x, y) in zip(dst, temp) if y is not None)
        data = [(path, owner, perm, now, now, now) for ((path, ), (owner, perm)) in zipped]
        cur.executemany(addsql, data)

def move_path(src, dst):
    now = datetime.datetime.now()

    src = convert_many(src)
    dst = convert_many(dst)
    assert len(src) == len(dst)

    data = [(x, y, now) for ((x, ), (y, )) in zip(dst, src)]

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.executemany("UPDATE metadata SET path = ?, modified = ? WHERE path = ?", data)

def delete_path(path):
    path = convert_many(path)
    delsql = 'DELETE FROM metadata WHERE path = ?'

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.executemany(delsql, path)

def calc_permission_string(number):
    base = 'rwxrwxrwx'
    number = str(number)
    binary = []
    for digit in number[:3]:
        binary.extend([int(y) for y in '{0:03b}'.format(int(digit))])
    return ''.join([b if (a and b) else '-' for a, b in zip(binary, base)])

def calc_permission_number(string):
    numbers = []
    string += '-' * (9 - len(string))
    for group in (string[:3], string[3:6], string[6:9]):
        a = ['1' if x and x not in ["-", "0"] else '0' for x in group]
        numbers.append(int("0b" + ''.join(a), 2))
    return ''.join(numbers)

def validate_permission(value):
    full = 'rwxrwxrwx'
    assert len(value) == len(full)
    for l, f in zip(value, full):
        assert (l == '-') or (l == f)

def get_permission_string(path):
    return get_meta_data(path)[2]

def get_permission_number(path):
    return calc_permission_number(get_meta_data(path)[2])

def set_permission_string(path, value):
    number = calc_permission_number(value)
    set_permission_number(path, number)

def set_permission_number(path, value):
    now = datetime.datetime.now()

    validate_permission(value)

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET permission = ?, modified = ? WHERE path = ?", (value, now, path))

def set_permission(path, value):
    try:
        set_permission_number(path, value)
    except ValueError:
        set_permission_string(path, value)

def set_time(path, value=None):
    if type(value) == dict:
        set_time_dict(path, value)
    elif type(value) == str:
        set_time_string(path, value)
    elif type(value) in (tuple, list):
        set_time_list(path, value)
    else:
        raise TypeError

def set_time_list(path, value):
    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    columns = ['accessed', 'created', 'modified']

    a = [x + ' = ?' for (x, y) in zip(columns, value) if y is not None]
    b = tuple(x for x in value if x is not None)
    upsql = "UPDATE metadata SET %s WHERE path = ?" % ', '.join(a)

    with con:
        cur = con.cursor()
        cur.execute(upsql, b + (path, ))

def set_time_dict(path, value=None):
    done = [None, None, None]
    d = {
        'a': 0, 'access': 0, 'accessed': 0,
        'm': 1, 'modify': 1, 'modified': 1,
        'c': 2, 'create': 2, 'created': 2
    }
    for key in value:
       done[d[key]] = value[key]
    set_time_list(path, done)


def set_time_string(path, value=None):
    # some magic that should not exist
    done = [None, None, None]
    d = {
        'a': 0,
        'c': 1,
        'm': 2
    }
    timeinc = {
        'w':'weeks',
        'd': 'days',
        'h':'hours',
        'm':'minutes',
        's':'seconds'
    }
    for time in value.split(','):
        time = time.strip()
        if time:
            lvl = time[0]
            try:
                other = float(time[1:-1])
            except ValueError:
                other = 0.0
            if len(time) >= 2:
                unit = time[-1]
            else:
                unit = 'n'

            if unit == 'y':
                unit = 'd'
                other *= year
            elif unit == 'n':
                unit = 'd'
                other = 0.0
            delta = datetime.timedelta(**{timeinc[unit]: other})
            if done[d[lvl]] is None:
                done[d[lvl]] = delta
            else:
                done[d[lvl]] += delta

    done = [x + datetime.datetime.now() if x is not None else None for x in done]
    set_time_list(path, done)

def get_time(path):
    return get_meta_data(path)[3:6]

def get_owner(path):
    return get_meta_data(path)[1]

def validate_owner(owner):
    pass

def set_owner(path, owner):
    now = datetime.datetime.now()

    value = validate_owner(value)

    con = sqlite3.connect(METADATAFILE,  detect_types=sqlite3.PARSE_DECLTYPES)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET owner = ?, modified = ? WHERE path = ?", (value, path, now))
