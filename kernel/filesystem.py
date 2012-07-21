import os
import shutil
import imp
import glob

from kernel.constants import BASEPATH, METADATAFILE
import kernel.metadata
import kernel.userdata

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
    return os.path.dirname(abs_path(path))

def base_name(path):
    return os.path.basename(abs_path(path))

def split(path):
    return dir_name(path), base_name(path)

#######################################

def exists(caller, path):
    return os.path.exists(abs_path(path))

def is_file(caller, path):
    return os.path.isfile(abs_path(path))

def is_dir(caller, path):
    return os.path.isdir(abs_path(path))

def move(caller, src, dst):
    a = list_glob(join_path(src, "*")) + [src]
    shutil.move(abs_path(src), abs_path(dst))
    b = list_glob(join_path(dst, "*")) + [dst]
    kernel.metadata.move_path(a, b)

def copy(caller, src, dst, recursive=False):
    if recursive:
        shutil.copytree(abs_path(src), abs_path(dst))
        a = list_glob(join_path(src, "*")) + [src]
        b = list_glob(join_path(dst, "*")) + [dst]
        kernel.metadata.copy_path(a, b)
    else:
        shutil.copy2(abs_path(src), abs_path(dst))
        kernel.metadata.copy_path(src, dst)

def remove(caller, path, recursive=False):
    if recursive:
        shutil.rmtree(abs_path(path))
        a = list_glob(join_path(path, "*")) + [path]
        kernel.metadata.delete_path(a)
    else:
        os.remove(abs_path(path))
        kernel.metadata.delete_path(path)

def get_size(caller, path):
    return os.path.getsize(abs_path(path))

def list_dir(caller, path):
    return sorted(x for x in os.listdir(abs_path(path)) if ".git" not in x and not x.endswith(".pyc"))

def list_glob(expression):
    return [iabs_path(x) for x in glob.glob(abs_path(expression))]

def list_all(caller, path="/"):
    listing = [path]
    for x in list_dir(caller, path):
        new = join_path(path, x)
        if is_dir(caller, new):
            listing.extend(list_all(caller, new))
        else:
            listing.append(new)
    return listing

def make_dir(caller, path, parents=False):
    if parents:
        if not is_dir(caller, path):
            try:
                os.mkdir(abs_path(path))
            except OSError:
                make_dir(os.path.dirname(path), parents)
                os.mkdir(abs_path(path))
            kernel.metadata.add_path(path, "root", "rwxrwxrwx")
    else:
        os.mkdir(abs_path(path))
        kernel.metadata.add_path(path, "root", "rwxrwxrwx")

def open_file(caller, path, mode):
    temp = not is_file(caller, path)
    x = FileDecorator(caller, open(abs_path(path), mode), path)
    if temp:
        kernel.metadata.add_path(path, "root", "rwxrwxrwx")
    return x

def open_program(caller, path):
    x = abs_path(path)
    try:
        try:
            program = imp.load_source('program', '%s.py' % (x, ))
        except IOError:
            program = imp.load_source('program', x)
    except IOError:
        program = False
    return program


class FileDecorator(object):
    def __init__(self, caller, f, name):
        self.__f = f
        self.__name = name
        self.__caller = caller
        kernel.metadata.set_time(self.__caller, self.name, 'an')

    def close(self):
        kernel.metadata.set_time(self.__caller, self.name, 'mn')
        self.__f.close()

    @property
    def name(self):
        return self.__name

    def __getattr__(self, name):
        return getattr(self.__f, name)

    def __iter__(self):
        return self.__f.__iter__()
    def __repr__(self):
        return self.__f.__repr__()
    def __enter__(self):
        return self.__f.__enter__()
    def __exit__(self, *excinfo):
        return self.__f.__exit__(self, *excinfo)

def has_permission(path, user, access):
    owner = kernel.metadata.get_owner(path)
    permissions = kernel.metadata.get_permission_number(path)
    # TODO # add groups
    # TODO # add superuser
    d = {'r': 4, 'w': 2, 'x': 1}
    compare = [d[access] * (owner == user), 0, d[access]]
    return any(int(x) & y for (x, y) in zip(permissions, compare))