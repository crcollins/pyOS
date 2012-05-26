import re

import kernel.filesystem as fs
from kernel.system import System
from kernel.constants import OSNAME, RUNNING, PIPECHAR, VARCHAR, \
        INCHAR, OUTCHAR, APPENDCHAR

varparse = re.compile(r"\%s\w*" % (VARCHAR, ))
stdioparse = re.compile(r"([%s%s]+\s*\w+)" % (OUTCHAR, INCHAR))
quoteparse = re.compile(r"""(\"[^\"]*\"|\'[^\']*\'|\|)""")

def run(shell, args):
    while System.state >= RUNNING:
        data = raw_input("root@%s:%s$ "% (OSNAME, shell.path))
        data = data.strip()
        if data:
            shell.prevcommands.append(data)
            try:
                programs = eval_input(shell, data)
                shells = start_shells(shell, programs)
                connect_shells(shells)
                for x in shells:
                    x.run()
            except IndexError:
                pass

def quote_split(string):
    a = []
    for x in re.split(quoteparse, string):
        if not x.startswith("'") and not x.startswith('"'):
            a.extend(x.strip().split())
        else:
            a.append(x)
    return a

def eval_input(shell, string):
    #replace $vars
    string = re.sub(varparse, shell.get_var, string)
    a = quote_split(string)

    b = [[None, [], None, None]]
    state = None
    charstates = [APPENDCHAR, OUTCHAR, INCHAR, PIPECHAR]
    for part in a:
        if part in charstates and state in charstates:
            raise SyntaxError
        elif part in charstates:
            state = part
        else:
            if state in [None, PIPECHAR]:
                if state == PIPECHAR:
                    b.append([None, [], None, None])
                if part in shell.aliases:
                    part = shell.aliases[part]
                b[-1][0] = part         # program
            elif state == "args":
                b[-1][1].append(part)   # args
            elif state == INCHAR and not b[-1][2]:
                b[-1][2] = part         # stdin
            elif state == OUTCHAR and not b[-1][3]:
                b[-1][3] = (part, 'w')  # stdout
            elif state == APPENDCHAR and not b[-1][3]:
                b[-1][3] = (part, 'a')  #stdout append
            state = "args"
    # [[program, [arg0, arg1, ...], cin, (cout, mode)], ...]
    return b

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
