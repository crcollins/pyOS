import kernel.filesystem
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
        path = self.filesystem.join_path(KERNELDIR, "startup")
        program = self.new_shell(program=path)
        program.run()

    def shutdown(self):
        path = self.filesystem.join_path(KERNELDIR, "shutdown")
        program = self.new_shell(program=path)
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

    def exists(self, path):
        return self.fs.exists(self, path)
    def is_file(self, path):
        return self.fs.is_file(self, path)
    def is_dir(self, path):
        return self.fs.is_dir(self, path)
    def move(self, src, dst):
        return self.fs.move(self, src, dst)
    def copy(self, src, dst, recursive=False):
        return self.fs.copy(self, src, dst, recursive)
    def remove(self, path, recursive=False):
        return self.fs.remove(self, path, recursive)
    def get_size(self, path):
        return self.fs.get_size(self, path)
    def list_dir(self, path):
        return self.fs.list_dir(self, path)
    def list_glob(self, expression):
        return self.fs.list_glob(self, expression)
    def list_all(self, path="/"):
        return self.fs.list_all(self, path)
    def make_dir(self, path, parents=False):
        return self.fs.make_dir(self, path, parents)
    def open_file(self, path, mode):
        return self.fs.open_file(self, path, mode)
    def open_program(self, path):
        return self.fs.open_program(self, path)

    def get_meta_data(self, path):
        return self.md.get_meta_data(self, path)
    def get_all_meta_data(self, path='/'):
        return self.md.get_all_meta_data(self, path)
    def get_permission_string(self, path):
        return self.md.get_permission_string(self, path)
    def get_permission_number(self, path):
        return self.md.get_permission_number(self, path)
    def set_permission_string(self, path, value):
        return self.md.set_permission_string(self, path, value)
    def set_permission_number(self, path, value):
        return self.md.set_permission_number(self, path, value)
    def set_permission(self, path, value):
        return self.md.set_permission(self, path, value)
    def set_time(self, path, value=None):
        return self.md.set_time(self, path, value)
    def set_time_list(self, path, value):
        return self.md.set_time_list(self, path, value)
    def set_time_dict(self, path, value=None):
        return self.md.set_time_dict(self, path, value)
    def set_time_string(self, path, value=None):
        return self.md.set_time_string(self, path, value)
    def get_time(self, path):
        return self.md.get_time(self, path)
    def get_owner(self, path):
        return self.md.get_owner(self, path)
    def set_owner(self, path, owner):
        return self.md.set_owner(self, path, owner)

    def get_user_data(self, user):
        return self.ud.get_user_data(self, user)
    def get_all_user_data(self, ):
        return self.ud.get_all_user_data(self, )
    def add_user(self, user, group, info, homedir, shell, password):
        return self.ud.add_user(self, user, group, info, homedir, shell, password)
    def delete_user(self, user):
        return self.ud.delete_user(self, user)
    def change_user(self, user, value):
        return self.ud.change_user(self, user, value)
    def get_group(self, user):
        return self.ud.get_group(self, user)
    def set_group(self, user, value):
        return self.ud.set_group(self, user, value)
    def get_info(self, user):
        return self.ud.get_info(self, user)
    def set_info(self, user, value):
        return self.ud.set_info(self, user, value)
    def get_homedir(self, user):
        return self.ud.get_homedir(self, user)
    def set_homedir(self, user, value):
        return self.ud.set_homedir(self, user, value)
    def get_shell(self, user):
        return self.ud.get_shell(self, user)
    def set_shell(self, user, value):
        return self.ud.set_shell(self, user, value)
    def get_password(self, user):
        return self.ud.get_password(self, user)
    def set_password(self, user, value):
        return self.ud.set_password(self, user, value)
    def correct_password(self, user, password):
        return self.ud.correct_password(self, user, password)