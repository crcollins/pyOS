import re

import kernel.filesystem
import kernel.stream
import kernel.system

class Shell(object):
    def __init__(self, pid, parent=None, program="interpreter", args="",
                 stdin=None, path="/"):
        self.programname = program
        self.args = args

        self.path = path
        self.parent = parent
        self.pid = pid

        if self.parent:
            self.vars = self.parent.vars.copy()
            self.aliases = self.parent.aliases.copy()
            self.prevcommands = self.parent.prevcommands[:]
        else:
            self.vars = {"PATH":"/programs"}
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
            self.stderr.write("%s: command not found\n" %self.programname)

        #cleanup
        self.stdout.close()
        self.stderr.close()
        kernel.system.System.kill(self)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = self.iabs_path(path)

    def iabs_path(self, path):
        if path[0] != '/':
            if path[0:2] == "./":
                path = path[2:]
            path = kernel.filesystem.join_path(self.path, path)
        return '/' + kernel.filesystem.eval_path(path)

    def irel_path(self, path, base=None):
        if base is None:
            base = self.path
        return kernel.filesystem.rel_path(self.iabs_path(path), self.iabs_path(base))

    def program_paths(self, name):
        if name[0:2] == "./":
            a = [self.iabs_path(name)]
        else:
            paths = self.get_var('PATH').split(':')
            a = [kernel.filesystem.join_path(x, name) for x in paths]
        return a

    def get_var(self, name):
        try:
            x = self.vars[name.group(0).lstrip("$")]
        except AttributeError:
            x = self.vars[name.lstrip("$")]
        except:
            x = ''
        return x

    def set_var(self, name, value):
        self.vars[name] = value

    def find_program(self, name):
        for x in self.program_paths(name):
            program = kernel.filesystem.open_program(x)
            if program:
                break
        return program

    def __repr__(self):
        return "<Shell(pid=%d, program=%s, args=%s, path=%s)>" %(self.pid, self.programname, self.args, self.path)

    def __str__(self):
        return "<%s %d>" %(self.programname, self.pid)