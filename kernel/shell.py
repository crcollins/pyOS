import re

import kernel.filesystem
import kernel.stream

class Shell(object):
    def __init__(self, pid, parent=None, program="interpreter", args="",
                 stdin='', currentpath="/"):
        self.program = program
        self.args = args

        self.curpath = currentpath
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

        if type(stdin) == str:
            self.stdin = kernel.stream.Stream(value=stdin, kind="in")
        else:
            self.stdin = stdin
        self.stdout = kernel.stream.Stream(kind="out")
        self.stderr = kernel.stream.Stream(kind="err")

    def run(self):
        try:
            self.run_program(self.program, self.args)
        except Exception, e:
            self.stdout.write("We had an error Admiral.")
            self.stdout.write(e)

    def get_curpath(self):
        return self.curpath

    def set_curpath(self, path):
        self.curpath = self.iabs_path(path)

    def iabs_path(self, path):
        if path[0] != '/':
            if path[0:2] == "./":
                path = path[2:]
            path = kernel.filesystem.join_path(self.curpath, path)
        return '/' + kernel.filesystem.eval_path(path)

    def irel_path(self, path, base=None):
        if base is None:
            base = self.curpath
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

    def run_program(self, name, args):
        for x in self.program_paths(name):
            program = kernel.filesystem.open_program(x)
            if program:
                program.run(self, args)
                break
        if not program:
            #self.stderr.put("%s: command not found" %name)
            print "%s: command not found" %name