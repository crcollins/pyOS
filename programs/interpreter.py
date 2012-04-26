import kernel.filesystem
from kernel.system import System

import re

varparse = re.compile(r"\$\w*")
pipeparse = re.compile(r"(\>+\d?|\<+|\|)")

def run(shell, args):
    while System.state >= 1:
        data = raw_input("root@pyOS:%s$ "%shell.path)
        try:
            programs, relations = eval_input(shell, data)
            listing = start_shells(shell, programs)
            for x in listing:
                x.run()
        except IndexError:
            pass

def eval_input(shell, string):
    #replace $vars
    string = re.sub(varparse, shell.get_var, string)
    split = re.split(pipeparse, string)

    programs = []
    for x in split[::2]:
        parts = x.strip().split(' ')
        if kernel.filesystem.is_directory(shell.iabs_path(parts[0])):
            print "Is a directory"
        if parts[0] in shell.aliases:
            parts[0] = shell.aliases[parts[0]]
        programs.append((parts[0], parts[1:])) #(program, [args])

    relations = []
    #hack to split commands into (commandidx, op, command2idx) groups
    for num in xrange(len(split)/2 - (not len(split)%2)):
        relations.append((num*2, split[num*2+1], num*2+1))

    return programs, relations

def start_shells(shell, programs):
    parent = shell
    currentpath = shell.path

    listing = []
    for (program, args) in programs:
        x = System.new_shell(parent=parent, currentpath=currentpath,
                         program=program, args=args)
        listing.append(x)
    return listing

def connect_shells(programs, relations):
    pass

def help():
    return "HELP"