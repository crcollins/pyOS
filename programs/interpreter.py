import kernel.filesystem
from kernel.system import System

import re

varparse = re.compile(r"\$\w*")
stdioparse = re.compile(r"([<>]+\s*\w+)")

def run(shell, args):
    while System.state >= 1:
        data = raw_input("root@pyOS:%s$ "%shell.path)
        try:
            programs = eval_input(shell, data)
            shells, programs = start_shells(shell, programs)
            connect_shells(shells, programs)
            for x in shells:
                x.run()
        except IndexError:
            pass

def eval_input(shell, string):
    #replace $vars
    string = re.sub(varparse, shell.get_var, string)

    #split pipes/stdio
    split = string.split("|")
    programsplit = (re.split(stdioparse, x) for x in split)
    cleaned = [[y.strip() for y in x if y.strip()] for x in programsplit]

    fs = kernel.filesystem

    #format them things
    final = []
    for pipeset in cleaned:
        program = pipeset[0]
        if program in shell.aliases:
            program = shell.aliases[program]
        args, cin, cout = [], [], []
        for part in pipeset[1:]:
            p2 = part.lstrip("<>")
            if ">" in part:
                cout.append(fs.open_file(p2, "w"))
            elif ">>" in part:
                cout.append(fs.open_file(p2, "a"))
            elif "<" in part:
                cin.append(p2)
            else:
                args.extend(part.split())
        final.append((program, args, cin, cout))
    #((program, [arg0, arg1, ...], [Fcin0, Fcin1, ...], [Fcout0, Fcout1, ...]), ...)
    return final

def start_shells(shell, programs):
    parent = shell
    path = shell.path

    listing = []
    newprograms = []
    for (program, args, cin, cout) in programs:
        newshell = System.new_shell(parent=parent, path=path,
                         program=program, args=args)
        #hack to convert the cin into streams from cat.
        newcin = [System.new_shell(parent=parent, path=path,
                         program="cat", args=[x]) for x in cin]
        listing.append(newshell)
        newprograms.append((program, args, newcin, cout))
    return listing, newprograms

def connect_shells(shells, programs):
    #connect all of the cins and couts
    for i, (program, args, cins, couts) in enumerate(programs):
        program = shells[i]
        list((x.stdout.add(program.stdin, stream=True) for x in cins))
        list((program.stdout.add(x.write, stream=False) for x in couts))
    #connect the seperate programs
    for i, p1 in enumerate(shells[1:]):
        p0 = shells[i]
        p0.stdout.add(p1.stdin, stream=True)

def help():
    return "HELP"