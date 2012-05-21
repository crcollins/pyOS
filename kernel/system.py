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
        self.output = None
        self.pids = []
        self.state = IDLE

    def run(self):
        self.startup()
        self.state = IDLE
        while self.state >= IDLE:
            current = self.new_shell()
            current.run()
        self.shutdown()
        if self.state == REBOOT:
            self.run()

    def startup(self):
        path = kernel.filesystem.join_path(KERNELDIR, "startup")
        try:
            program = kernel.filesystem.open_program(path)
            program.run()
        except:
            raise IOError

    def shutdown(self):
        path = kernel.filesystem.join_path(KERNELDIR, "shutdown")
        try:
            program = kernel.filesystem.open_program(path)
            program.run()
        except:
            raise IOError

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
