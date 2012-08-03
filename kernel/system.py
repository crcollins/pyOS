import kernel.filesystem
import kernel.metadata
import kernel.userdata

import kernel.shell
from kernel.constants import KERNELDIR, IDLE, REBOOT, RUNNING

class System(object):
    """
    Handles all of the low level stuff.
    PIDs, startup, shutdown, events

    System States:
    -2: reboot
    -1: shutting down
    0:  idle
    1:  running shell
    """
    _state = {}

    def __init__(self):
        self.__dict__ = self._state
        self.display = None  # Display()

        self.filesystem = kernel.filesystem
        self.metadata = kernel.metadata
        self.userdata = kernel.userdata

        self.pids = []
        self.state = IDLE

    def run(self):
        self.startup()
        self.state = IDLE
        while self.state >= IDLE:
            current = self.new_shell(program='login')
            current.run()
        self.shutdown()
        if self.state == REBOOT:
            self.run()

    def startup(self):
        path = self.filesystem.join_path(KERNELDIR, "startup.py")
        program = self.filesystem.open_program(path)
        program.run()

    def shutdown(self):
        path = self.filesystem.join_path(KERNELDIR, "shutdown.py")
        program = self.filesystem.open_program(path)
        program.run()

    def new_shell(self, *args, **kwargs):
        y = kernel.shell.Shell(len(self.pids), *args, **kwargs)
        self.new_pid(y)
        self.state = RUNNING
        return y

    def get_pid(self, item):
        try:
            x = self.pids.index(item)
        except:
            x = None
        return x

    def get_process(self, pid):
        try:
            x = self.pids[pid]
        except:
            x = None
        return x

    def new_pid(self, item):
        x = len(self.pids)
        self.pids.append(item)
        return x

    def get_events(self, _type=None):
        if _type is None:
            return "all"
        else:
            return "some"

    def kill(self, shell):
        self.pids.remove(shell)

System = System()

def compare_permission(path, user, access):
    owner = System.metadata.get_owner(path)
    permissions = System.metadata.get_permission_number(path)
    if type(access) == int:
        compare = [access * (user == owner), 0, access]
    else:
        d = {'r': 4, 'w': 2, 'x': 1}
        compare = [d[access] * (owner == user), 0, d[access]]
    return any(int(x) & y for (x, y) in zip(permissions, compare))

def has_permission(path, user, access):
    dirpaths = [path]
    temppath = path
    while temppath != '/':
        temppath = System.filesystem.dir_name(temppath)
        dirpaths.append(temppath)
    if not all(compare_permission(x, user, 5) for x in dirpaths[1:]):
        return False

    if System.filesystem.is_dir(dirpaths[0]):
        if not compare_permission(dirpaths[0], user, access):
            return False
    else:
        if not compare_permission(dirpaths[1], user, access):
            return False
        try:
            compare_permission(dirpaths[0], user, access)
        except TypeError:
            if access != 'w':
                return False
    return True

def check_permission(amount, access):
    def real_decorator(function):
        def wrapper(self, *args, **kwargs):
            checkpaths = args[:amount]
            laccess = access # hack to fix UnboundLocalError
            if type(laccess) == int:
                laccess = list(set(args[laccess]) & {'r', 'w'})[0]
            for path in checkpaths:
                if has_permission(path, 'root', laccess):
                    print "root %s has permisison on file(s) %s" % (laccess, str(checkpaths))
                else:
                    print "root %s permission denied for file(s) %s" % (laccess, str(checkpaths))
            return function(self, *args, **kwargs)
        return wrapper
    return real_decorator


class SysCall(object):
    def __init__(self, shell):
        self.fs = System.filesystem
        self.md  = System.metadata
        self.ud= System.userdata
        self.shell = shell

    def abs_path(self, path):
        return self.fs.abs_path(path)
    def rel_path(self, path, base):
        return self.fs.rel_path(path, base)
    def irel_path(self, path):
        return self.fs.irel_path(path)
    def iabs_path(self, path):
        return self.fs.iabs_path(path)
    def dir_name(self, path):
        return self.fs.dir_name(path)
    def base_name(self, path):
        return self.fs.base_name(path)
    def split(self, path):
        return self.fs.split(path)
    def join_path(self, *args):
        return self.fs.join_path(*args)

    #############################################

    @check_permission(1, 'r')
    def exists(self, path):
        return self.fs.exists(path)

    @check_permission(1, 'r')
    def is_file(self, path):
        return self.fs.is_file(path)

    @check_permission(1, 'r')
    def is_dir(self, path):
        return self.fs.is_dir(path)

    @check_permission(2, 'w')
    def move(self, src, dst):
        a, b = self.fs.move(src, dst)
        self.md.move_path(a, b)

    @check_permission(2, 'w')
    def copy(self, src, dst, recursive=False):
        a, b = self.fs.copy(src, dst, recursive)
        self.md.copy_path(a, b)

    @check_permission(1, 'w')
    def remove(self, path, recursive=False):
        a = self.fs.remove(path, recursive)
        self.md.delete_path(a)

    @check_permission(1, 'r')
    def get_size(self, path):
        return self.fs.get_size(path)

    @check_permission(1, 'r')
    def list_dir(self, path):
        return self.fs.list_dir(path)

    @check_permission(1, 'r')
    def list_glob(self, expression):
        return self.fs.list_glob(expression)

    @check_permission(1, 'r') # ? #
    def list_all(self, path="/"):
        listing = [path]
        for x in self.list_dir(path):
            new = self.join_path(path, x)
            if self.is_dir(new):
                listing.extend(self.list_all(new))
            else:
                listing.append(new)
        return listing

    @check_permission(1, 'w')
    def make_dir(self, path):
        self.fs.make_dir(path)
        self.md.add_path(path, "root", "rwxrwxrwx")

    @check_permission(1, 1)
    def open_file(self, path, mode):
        temp = self.fs.is_file(path)
        x = FileDecorator(self.fs.open_file(path, mode), path)
        if not temp:
            self.md.add_path()
        return x

    @check_permission(1, 'x')
    def open_program(self, path):
        return self.fs.open_program(path)

    #############################################

    @check_permission(1, 'r')
    def get_meta_data(self, path):
        return self.md.get_meta_data(path)

    @check_permission(1, 'r') # ? #
    def get_all_meta_data(self, path='/'):
        return self.md.get_all_meta_data(path)

    @check_permission(1, 'r')
    def get_permission_string(self, path):
        return self.md.get_permission_string(path)

    @check_permission(1, 'r')
    def get_permission_number(self, path):
        return self.md.get_permission_number(path)

    @check_permission(1, 'w')
    def set_permission_string(self, path, value):
        return self.md.set_permission_string(path, value)

    @check_permission(1, 'w')
    def set_permission_number(self, path, value):
        return self.md.set_permission_number(path, value)

    @check_permission(1, 'w')
    def set_permission(self, path, value):
        return self.md.set_permission(path, value)

    @check_permission(1, 'w')
    def set_time(self, path, value=None):
        return self.md.set_time(path, value)

    @check_permission(1, 'w')
    def set_time_list(self, path, value):
        return self.md.set_time_list(path, value)

    @check_permission(1, 'w')
    def set_time_dict(self, path, value=None):
        return self.md.set_time_dict(path, value)

    @check_permission(1, 'w')
    def set_time_string(self, path, value=None):
        return self.md.set_time_string( path, value)

    @check_permission(1, 'r')
    def get_time(self, path):
        return self.md.get_time(path)

    @check_permission(1, 'r')
    def get_owner(self, path):
        return self.md.get_owner(path)

    @check_permission(1, 'w')
    def set_owner(self, path, owner):
        return self.md.set_owner(path, owner)

    #############################################

    def get_user_data(self, user):
        return self.ud.get_user_data(user)
    def get_all_user_data(self):
        return self.ud.get_all_user_data()
    def add_user(self, user, group, info, homedir, shell, password):
        return self.ud.add_user(user, group, info, homedir, shell, password)
    def delete_user(self, user):
        return self.ud.delete_user(user)
    def change_user(self, user, value):
        return self.ud.change_user(user, value)
    def get_group(self, user):
        return self.ud.get_group(user)
    def set_group(self, user, value):
        return self.ud.set_group(user, value)
    def get_info(self, user):
        return self.ud.get_info(user)
    def set_info(self, user, value):
        return self.ud.set_info(user, value)
    def get_homedir(self, user):
        return self.ud.get_homedir(user)
    def set_homedir(self, user, value):
        return self.ud.set_homedir(user, value)
    def get_shell(self, user):
        return self.ud.get_shell(user)
    def set_shell(self, user, value):
        return self.ud.set_shell(user, value)
    def get_password(self, user):
        return self.ud.get_password(user)
    def set_password(self, user, value):
        return self.ud.set_password(user, value)
    def correct_password(self, user, password):
        return self.ud.correct_password(user, password)


class FileDecorator(object):
    def __init__(self, f, name):
        self.__f = f
        self.__name = name
        System.metadata.set_time(self.name, 'an')

    def close(self):
        System.metadata.set_time(self.name, 'mn')
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
