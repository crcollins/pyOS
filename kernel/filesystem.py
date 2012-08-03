import os
import shutil
import imp
import glob

from kernel.constants import BASEPATH

def abs_path(path):
    # returns external absolute path
    return os.path.abspath(os.path.join(BASEPATH, path.lstrip('/')))

def rel_path(path, base):
    # returns external relative path
    return os.path.relpath(path, base)

def irel_path(path):
    # returns internal relative path
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

def join_path(*args):
    return os.path.join(*args)

def dir_name(path):
    return os.path.dirname(path)

def base_name(path):
    return os.path.basename(path)

def split(path):
    return dir_name(path), base_name(path)

#######################################

def exists(path):
    return os.path.exists(abs_path(path))

def is_file(path):
    return os.path.isfile(abs_path(path))

def is_dir(path):
    return os.path.isdir(abs_path(path))

def move(src, dst):
    a = list_glob(join_path(src, "*")) + [src]
    shutil.move(abs_path(src), abs_path(dst))
    b = list_glob(join_path(dst, "*")) + [dst]
    return a, b

def copy(src, dst):
    shutil.copy2(abs_path(src), abs_path(dst))

def remove(path, recursive=False):
    if recursive:
        shutil.rmtree(abs_path(path))
        a = list_glob(join_path(path, "*")) + [path]
        return a
    else:
        os.remove(abs_path(path))
        return path

def get_size(path):
    return os.path.getsize(abs_path(path))

def list_dir(path):
    return sorted(x for x in os.listdir(abs_path(path)) if ".git" not in x and not x.endswith(".pyc"))

def list_glob(expression):
    return [iabs_path(x) for x in glob.glob(abs_path(expression))]

def list_all(path="/"):
    listing = [path]
    for x in list_dir(path):
        new = join_path(path, x)
        if is_dir(new):
            listing.extend(list_all(new))
        else:
            listing.append(new)
    return listing

def make_dir(path):
    os.mkdir(abs_path(path))

def open_file(path, mode):
    return open(abs_path(path), mode)

def open_program(path):
    x = abs_path(path)
    if not is_dir(path):
        try:
            program = imp.load_source('program', x)
        except IOError:
            program = False
    else:
        program = False
    return program


