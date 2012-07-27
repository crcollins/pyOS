import re

import kernel.stream
import kernel.system
from kernel.constants import PROGRAMSDIR, VARCHAR, BASEDIR

class Shell(object):
    def __init__(self, pid, parent=None, program="interpreter",
                 args="", stdin=None, path=BASEDIR):
        self.programname = program
        self.args = args

        self.__path = path
        self.__oldpath = path
        self.parent = parent
        self.pid = pid

        self.syscall = kernel.system.SysCall(self)

        if self.parent:
            self.vars = self.parent.vars.copy()
            self.aliases = self.parent.aliases.copy()
            self.prevcommands = self.parent.prevcommands[:]
        else:
            self.vars = {"PATH": PROGRAMSDIR,
                         "HOME": BASEDIR,
                         "PWD": self.__path,
                         "OLDPWD": self.__oldpath}
            self.aliases = dict()
            self.prevcommands = []

        self.stdin = stdin
        self.stdout = kernel.stream.Pipe(name="out", writer=self)
        self.stderr = kernel.stream.Pipe(name="err", writer=self)

    def run(self):
        self.program = self.find_program(self.programname)
        if self.program:
            self.program.run(self, self.args)
        else:
            # TODO # add back "is a directory"
            self.stderr.write("%s: command not found\n" % (self.programname, ))
        #cleanup
        self.stdout.close()
        self.stderr.close()
        kernel.system.System.kill(self)

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__oldpath = self.__path
        self.__path = self.sabs_path(path)

    def get_old_path(self):
        return self.__oldpath

    def sabs_path(self, path):
        if not path.startswith('/'):
            if path.startswith('./'):
                path = path[path.index('/') + 1:]
            path = self.syscall.join_path(self.get_path(), path)
        return self.syscall.iabs_path(path)

    def srel_path(self, path, base=None):
        if base is None:
            base = self.get_path()
        return self.syscall.rel_path(self.sabs_path(path),
                                          self.sabs_path(base))

    def program_paths(self, name):
        if name[0:2] == "./":
            a = [self.sabs_path(name)]
        else:
            paths = self.get_var('PATH').split(':')
            a = [self.syscall.join_path(x, name) for x in paths]
        return a

    def get_var(self, name):
        try:
            x = self.vars[name.group(0).lstrip(VARCHAR)]
        except AttributeError:
            x = self.vars[name.lstrip(VARCHAR)]
        except:
            x = ''
        return x

    def set_var(self, name, value):
        self.vars[name] = value

    def hist_find(self, value, start=True):
        done = ''
        for x in reversed(self.prevcommands):
            if start and x.startswith(value):
                done = x
                break
            elif not start and value in x:
                done = x
                break
        return done

    def find_program(self, name):
        for x in self.program_paths(name):
            if not x.endswith('.py'):
                x += '.py'
            program = self.syscall.open_program(x)
            if program:
                break
            else:
                program = self.syscall.open_program(x[:-3])
            if program:
                break
        return program

    def __repr__(self):
        return "<Shell(pid=%d, program=%s, args=%s, path=%s)>" % (self.pid,
                                    self.programname, self.args, self.path)

    def __str__(self):
        return "<%s %d>" % (self.programname, self.pid)
