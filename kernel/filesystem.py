import os
import shutil
import imp
import glob
import sqlite3

from kernel.constants import BASEPATH, METADATAFILE

def abs_path(path):
    # returns external absolute path
    return os.path.join(BASEPATH, path.lstrip('/'))

def rel_path(path, base):
    # returns external relative path
    return os.path.relpath(path, base)

def eval_path(path):
    # returns internal relative path
    path = path.strip('/') if path != '/' else '.'
    b = os.path.relpath(path, BASEPATH)
    if b in ('..', '.'):
        b = ''
    return b.replace('../', '')

def convert(path):
    # returns internal absolute path
    a = os.path.commonprefix([BASEPATH, os.path.abspath(path)])
    b = os.path.relpath(path, BASEPATH)
    if len(a) < len(BASEPATH) or b == '.':
        return '/'
    else:
        return '/%s' % (b, )

def exists(path):
    return os.path.exists(abs_path(path))

def is_file(path):
    return os.path.isfile(abs_path(path))

def is_directory(path):
    return os.path.isdir(abs_path(path))

def move(src, dst):
    shutil.move(abs_path(src), abs_path(dst))

def copy(src, dst, recursive=False):
    if recursive:
        shutil.copytree(abs_path(src), abs_path(dst))
    else:
        shutil.copy2(abs_path(src), abs_path(dst))

def remove(path, recursive=False):
    if recursive:
        shutil.rmtree(abs_path(path))
    else:
        os.remove(abs_path(path))

def join_path(*args):
    return os.path.join(*args)

def get_size(path):
    return os.path.getsize(abs_path(path))

def list_dir(path):
    return sorted(os.listdir(abs_path(path)))

def list_glob(expression):
    return [convert(x) for x in glob.glob(abs_path(expression))]

def list_all(path="/"):
    listing = []
    for x in list_dir(path):
        new = join_path(path, x)
        if is_directory(new):
            listing.extend(list_all(new))
        else:
            listing.append(new)
    return listing

def make_dir(path):
    return os.mkdir(abs_path(path))

def open_file(path, mode):
    return open(abs_path(path), mode)

def open_program(path):
    x = abs_path(path)
    try:
        try:
            program = imp.load_source('program', '%s.py' % (x, ))
        except IOError:
            program = imp.load_source('program', x)
    except IOError:
        program = False
    return program

def dir_name(path):
    return os.path.dirname(abs_path(path))

def base_name(path):
    return os.path.basename(abs_path(path))

def split(path):
    return dir_name(path), base_name(path)

def build_meta_data_database():
    con = sqlite3.connect(abs_path(METADATAFILE))
    delsql = 'DELETE FROM metadata WHERE path = ?'
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?)'
    tablesql = '''CREATE TABLE IF NOT EXISTS metadata (
                    path TEXT,
                    ownerid INT,
                    permissions TEXT)'''
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT path FROM metadata")
            fsmatches = set(list_all())
            dbmatches = set(x[0] for x in cur.fetchall())

            for x in fsmatches.difference(dbmatches):
                cur.execute(addsql, ((x, 0, '777')))
            for x in dbmatches.difference(fsmatches):
                cur.execute(delsql, (x, ))

            con.commit()
    except:
        items = ((x, 0, '777') for x in list_all())
        with con:
            cur = con.cursor()
            cur.execute(tablesql)
            cur.executemany(addsql, items)
            con.commit()

def get_meta_data(path):
    con = sqlite3.connect(abs_path(METADATAFILE))
    data = None
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM metadata WHERE path = ?", (path, ))
        data = cur.fetchone()
        if data:
            ## to be added with users
            # cur.execute("SELECT username FROM users WHERE id = ?", (data[2], ))
            # data[2] = cur.fetchone()[0]
            ## force data to be strings and not unicode
            data = tuple(str(x) for x in data)
    return data

def _update_path(path, value):
    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET path = ? WHERE path = ?", (value, path))
        con.commit()

def _update_owner_id(path, value):
    value = check_owner_id(value)
    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET ownerid = ? WHERE path = ?", (value, path))
        con.commit()

def _update_permission(path, value):
    check_permission(value)
    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET permissions = ? WHERE path = ?", (value, path))
        con.commit()

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

def check_permission(value):
    for x in value:
        if 7 < int(x) or int(x) < 0:
            raise ValueError

def get_permission_string(path):
    return calc_permission_string(get_meta_data(path)[2])

def get_permission_number(path):
    return get_meta_data(path)[2]

def set_permission_string(path, value):
    number = calc_permission_number(value)
    _update_permissions(path, number)

def set_permission_number(path, value):
    _update_permissions(path, number)

def set_permission(path, value):
    try:
        set_permission_number(path, value)
    except ValueError:
        set_permission_string(path, value)

def get_owner_id(path):
    return get_meta_data(path)[1]

def get_owner_name(path):
    pass

def check_owner_id(owner):
    pass

def set_owner_id(path, owner):
    pass

def set_owner_name(path, owner):
    pass

def set_owner(path, owner):
    try:
        set_owner_id(path, owner)
    except ValueError:
        set_owner_id(path, owner)

