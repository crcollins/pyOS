import re

import kernel.filesystem
import kernel.stream

class Shell(object):
    def __init__(self, pid, parent=None, program="interpreter", args="",
                 stdin='', path="/"):
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

        self.stdin = kernel.stream.Stream(value=stdin, name="in", listeners=self.callback)
        self.stdout = kernel.stream.Stream(name="out")
        self.stderr = kernel.stream.Stream(name="err")

        self.program = self.find_program(self.programname)
        self.file = None

        if not self.program:
            self.file = kernel.filesystem.open_file(self.programname, "w")

    def callback(self, value):
        if self.file:
            self.file.write(value)
        else:
            pass

    def run(self):
        if self.program:
            self.program.run(self, self.args)
        elif not self.program and not self.stdin:
            self.stderr.write("%s: command not found" %self.programname)

        if self.file:
            self.file.close()

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