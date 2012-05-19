import os
import shutil
import imp

from kernel.constants import BASEPATH

def abs_path(path):
    return os.path.join(BASEPATH, path.lstrip('/'))

def rel_path(path, base):
    return os.path.relpath(path, base)

def eval_path( path):
    #returns relative path
    path = path.strip('/') if path != '/' else '.'
    b = os.path.relpath(path, BASEPATH)
    if b in ('..', '.'):
        b = ''
    return b.replace('../','')

def convert(path):
    #returns relative path
    a = os.path.commonprefix([BASEPATH, os.path.abspath(path)])
    b = os.path.relpath(path, BASEPATH)
    if len(a) < len(BASEPATH) or b == '.':
        return '/'
    else:
        return '/%s' %b

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

def make_dir(path):
    return os.mkdir(abs_path(path))

def open_file(path, mode):
    return open(abs_path(path), mode)

def open_program(path):
    x = abs_path(path)
    try:
        try:
            program = imp.load_source('program', '%s.py' %x)
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