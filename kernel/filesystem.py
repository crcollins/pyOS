import os
import shutil
import imp
import glob
import argparse
import sqlite3

from kernel.constants import BASEPATH, METADATAFILE

def abs_path(path):
    # returns external absolute path
    return os.path.abspath(os.path.join(BASEPATH, path.lstrip('/')))

def rel_path(path, base):
    # returns external relative path
    return os.path.relpath(path, base)

def irel_path(path):
    # returns internal relative path
    path = abs_path(path)
    b = os.path.relpath(path, BASEPATH)
    b = b.replace('../', '')
    if b in ('..', '.'):
        b = ''
    return b

def iabs_path(path):
    # returns internal absolute path
    b = os.path.relpath(path, BASEPATH)
    c = irel_path(b)
    return join_path('/', c)

def exists(path):
    return os.path.exists(abs_path(path))

def is_file(path):
    return os.path.isfile(abs_path(path))

def is_directory(path):
    return os.path.isdir(abs_path(path))

def move(src, dst):
    shutil.move(abs_path(src), abs_path(dst))
    a = list_glob(join_path(src, "*")) + [src]
    b = list_glob(join_path(dst, "*")) + [dst]
    move_path(a, b)

def copy(src, dst, recursive=False):
    if recursive:
        shutil.copytree(abs_path(src), abs_path(dst))
        a = list_glob(join_path(src, "*")) + [src]
        b = list_glob(join_path(dst, "*")) + [dst]
        copy_path(a, b)
    else:
        shutil.copy2(abs_path(src), abs_path(dst))
        copy_path(src, dst)

def remove(path, recursive=False):
    if recursive:
        shutil.rmtree(abs_path(path))
        a = list_glob(join_path(path, "*")) + [path]
        delete_path(a)
    else:
        os.remove(abs_path(path))
        delete_path(path)

def join_path(*args):
    return os.path.join(*args)

def get_size(path):
    return os.path.getsize(abs_path(path))

def list_dir(path):
    return sorted(x for x in os.listdir(abs_path(path)) if ".git" not in x and not x.endswith(".pyc"))

def list_glob(expression):
    return [iabs_path(x) for x in glob.glob(abs_path(expression))]

def list_all(path="/"):
    listing = []
    for x in list_dir(path):
        new = join_path(path, x)
        if is_directory(new):
            listing.extend(list_all(new))
        else:
            listing.append(new)
    return listing

def list_all(path="/"):
    listing = []
    for x in list_dir(path):
        new = join_path(path, x)
        if is_directory(new):
            listing.append(new)
            listing.extend(list_all(new))
        else:
            listing.append(new)
    return listing

def make_dir(path, parents=False):
    if parents:
        if not is_directory(path):
            try:
                os.mkdir(abs_path(path))
            except OSError:
                make_dir(os.path.dirname(path), parents)
                os.mkdir(abs_path(path))
            add_path(path, "root", "777")
    else:
        os.mkdir(abs_path(path))
        add_path(path, "root", "777")

def open_file(path, mode):
    temp = not is_file(path)
    x = open(abs_path(path), mode)
    if temp:
        add_path(path, "root", "777")
    return x

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

class Parser(argparse.ArgumentParser):
    def __init__(self, program, name=None, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, prog=program, *args, **kwargs)
        if name is None:
            self.name = program
        else:
            self.name = name
        self.help = False

    def add_shell(self, shell):
        self.shell = shell

    def exit(self, *args, **kwargs):
        pass

    def print_usage(self, *args, **kwargs):
        try:
            self.shell.stderr.write(self.format_usage())
            self.help = True
        except AttributeError:
            pass

    def print_help(self, *args, **kwargs):
        try:
            self.shell.stdout.write(self.help_msg())
            self.help = True
        except AttributeError:
            pass

    def help_msg(self):
        return "%s\n\n%s" % (self.name, self.format_help())

def convert_many(start, *args):
    if type(start) not in (list, set, tuple):
        done = [(start, ) + args]
    else:
        done = [(x, ) + args for x in start]
    return done

def build_meta_data_database():
    delsql = 'DELETE FROM metadata WHERE path = ?'
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?)'
    tablesql = '''CREATE TABLE IF NOT EXISTS metadata (
                    path TEXT,
                    owner TEXT,
                    permission TEXT)'''

    con = sqlite3.connect(abs_path(METADATAFILE))
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT path FROM metadata")
            fsmatches = set(list_all())
            dbmatches = set(x[0] for x in cur.fetchall())

            for x in fsmatches.difference(dbmatches):
                cur.execute(addsql, ((x, "root", "777")))
            for x in dbmatches.difference(fsmatches):
                cur.execute(delsql, (x, ))

            con.commit()
    except:
        items = ((x, 'root', '777') for x in list_all())
        with con:
            cur = con.cursor()
            cur.execute(tablesql)
            cur.executemany(addsql, items)
            con.commit()

def get_meta_data(path):
    data = None

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM metadata WHERE path = ?", (path, ))
        data = cur.fetchone()
        if data:
            ## force data to be strings and not unicode
            data = tuple(str(x) for x in data)
    return data

def add_path(path, owner, permission):
    check_permission(permission)
    check_owner(owner)
    data = convert_many(path, owner, permission)
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?)'

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.executemany(addsql, data)

def copy_path(src, dst):
    src = convert_many(src)
    dst = convert_many(dst)
    assert len(src) == len(dst)
    selsql = 'SELECT owner,permission FROM metadata WHERE path = ?'
    addsql = 'INSERT INTO metadata VALUES (?, ?, ?)'

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        temp = []
        for x in src:
            cur.execute(selsql, x)
            temp.append(cur.fetchone())

        data = [(path, owner, perm) for ((path, ), (owner, perm)) in zip(dst, temp)]
        cur.executemany(addsql, data)

def move_path(src, dst):
    src = convert_many(src)
    dst = convert_many(dst)
    assert len(src) == len(dst)
    data = [(x, y) for ((x, ), (y, )) in zip(dst, src)]

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.executemany("UPDATE metadata SET path = ? WHERE path = ?", data)
        con.commit()

def delete_path(path):
    path = convert_many(path)
    delsql = 'DELETE FROM metadata WHERE path = ?'

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.executemany(delsql, path)

def _update_owner(path, value):
    value = check_owner(value)

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET owner = ? WHERE path = ?", (value, path))
        con.commit()

def _update_permission(path, value):
    check_permission(value)

    con = sqlite3.connect(abs_path(METADATAFILE))
    with con:
        cur = con.cursor()
        cur.execute("UPDATE metadata SET permission = ? WHERE path = ?", (value, path))
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
    _update_permission(path, number)

def set_permission_number(path, value):
    _update_permission(path, number)

def set_permission(path, value):
    try:
        set_permission_number(path, value)
    except ValueError:
        set_permission_string(path, value)

def get_owner(path):
    return get_meta_data(path)[1]

def check_owner(owner):
    pass

def set_owner(path, owner):
    _update_owner(path, owner)
