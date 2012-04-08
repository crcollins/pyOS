from kernel import filesystem
from kernel import shell

class Main(object):
    """
    Handles all of the low level stuff.
    PIDs, startup, shutdown, events
    """
    def __init__(self):
        #self.fs = FileSystem.FileSystem()
        self.display = None#Display()
        self.output = None
        self.pids = []
        self.state = 0

    def run(self):
        self.startup()
        while self.state >= 0:
            current = self.new_shell()
            current.run()
        self.shutdown()

    def startup(self):
        try:
            program = filesystem.open_program('kernel/startup')
            program.run()
        except:
            raise IOError

    def shutdown(self):
        try:
            program = filesystem.open_program('kernel/shutdown')
            program.run()
        except:
            raise IOError

    def new_shell(self):
        x = self.new_pid(shell.Shell(len(self.pids)))
        return self.pids[x]

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
        x =  len(self.pids)
        self.pids.append(item)
        return x

    def get_events(self, _type=None):
        if _type is None:
            return "all"
        else:
            return "some"