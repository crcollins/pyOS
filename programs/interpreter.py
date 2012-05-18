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
            shells = start_shells(shell, programs)
            connect_shells(shells)
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
        #hack to extract the program name
        program = pipeset[0].split()[0]
        pipeset = pipeset[0].split()[1:] + pipeset[1:]

        if program in shell.aliases:
            program = shell.aliases[program]
        args, cin, cout = [], None, None
        #reversed so that the operators near the command take precedence
        for part in pipeset[::-1]:
            p2 = part.lstrip("<> ")
            if ">>" in part:
                cout = ((p2, "a"))
            elif ">" in part:
                cout = ((p2, "w"))
            elif "<" in part:
                cin = p2
            else:
                args.extend(part.split())
        final.append((program, args, cin, cout))
    #((program, [arg0, arg1, ...], cin, (cout, mode)), ...)
    return final

def start_shells(parent, programs):
    path = parent.path

    proper = []
    for (programname, args, cin, cout) in programs:
        #hack to convert cin into streams from cat.
        if cin:
            newcin = System.new_shell(parent=parent, path=path,
                         program="cat", args=[cin])
        else:
            newcin = cin

        newshell = System.new_shell(parent=parent, stdin=newcin, path=path,
                program=programname, args=args)

        #hack to convert cout into streams to write
        if cout:
            newcout = System.new_shell(parent=parent, stdin=newcin, path=path,
                         program="write", args=cout)
        else:
            newcout = cout
        proper.extend([x for x in [newcin, newshell, newcout] if x])
    #(Scin0, shell0, Scout0, Scin1 ...)
    return proper

def connect_shells(shells):
    #connect the seperate programs
    for p0, p1 in zip(shells[:-1], shells[1:]):
        p0.stdout.set_reader(p1)

def help():
    a = """
    Interpreter

    The main interface for the computer.

    usage: interpreter
    """
    return a