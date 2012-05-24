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

def build_metadata_database():
    #pseudocode
    con = sqlite3.connect(abs_path(METADATAFILE))
    try:
        with con:
            cur = con.cursor()
            cur.execute("SELECT path FROM metadata")
            matches = cur.fetchall()
            for x in list_all():
                #1-tuple because the matches are stored in 1-tuples
                if (x, ) not in matches:
                    print x
                    cur.execute('INSERT INTO metadata VALUES (NULL, ?, ?, ?)', ((x, 0, '777')))
            con.commit()
    except:
        items = ((x, 0, '777') for x in list_all())
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS metadata (id INTEGER PRIMARY KEY, path TEXT, ownerid INT, permissions TEXT)")
            cur.executemany('INSERT INTO metadata VALUES (NULL, ?, ?, ?)', items)
            con.commit()

def get_metadata(path):
    pass

def get_permission_number(path):
    ''.join([str(int(x)) for x in permissions])
    pass


def permissions_to_list(permissions):
    a = []
    for x in permissions:
        a.extend([int(y) for y in bin(int(x))[2:]])
    return a

def get_permission_number(path):
    pass

def get_permission_string(path):
    base = 'rwxrwxrwx'
    permissions = [1] * 9
    return ''.join([b if all(a and b) else '-' for a, b in zip(permissions, base)])
