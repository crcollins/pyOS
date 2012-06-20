import re

import kernel.filesystem as fs
from kernel.system import System
from kernel.constants import OSNAME, RUNNING, PIPECHAR, VARCHAR, \
        INCHAR, OUTCHAR, APPENDCHAR

varparse = re.compile(r"\%s\w*" % (VARCHAR, ))
stdioparse = re.compile(r"([%s%s]+\s*\w+)" % (OUTCHAR, INCHAR))
quoteparse = re.compile(r"""(\"[^\"]*\"|\'[^\']*\'|\|)""")
subparse = re.compile(r"""s(?P<lim>.)(.*?)(?P=lim)(.*?)(?P=lim)""")
bangparse = re.compile(r"""(\!+[^!]*)""")
# r"""(\!\!|(?<!\\)\![^!\s]*|\s+)"""

def run(shell, args):
    user = shell.get_var('USER')
    while System.state >= RUNNING:
        data = raw_input("%s@%s:%s$ "% (user, OSNAME, shell.path))
        data = data.strip()
        if data:
            cleaned, command = shell_expansion(shell, data)
            shell.prevcommands.append(command)

            programs = eval_input(shell, cleaned)
            shells = start_shells(shell, programs)

            for x in shells:
                x.run()

def quote_split(string):
    a = []
    for x in re.split(quoteparse, string):
        if not x.startswith("'") and not x.startswith('"'):
            a.extend(x.strip().split())
        else:
            a.append(x)
    return a

def get_hist(shell, value):
    if ':' in value:
        search, word = value.split(':')
    elif value[0] in "$^*":
        word = value
        search = ''
    else:
        word = ''
        search = value

    command = ''
    if search:
        if search.startswith('!'):
            command = shell.prevcommands[-1]
        elif search.startswith('?'):
            command = shell.hist_find(search[1:], False)
        elif search.isdigit() or (search.startswith('-') and search[1:].isdigit()):
            command = shell.prevcommands[int(search)]
        else:
            command = shell.hist_find(search)
    
    d = {
        '$': lambda : slice(-1, None),
        '^': lambda : slice(1, 2),
        '*': lambda : slice(1, None),
        '-': lambda x, y: slice(x, y)
    }
    execute = True
    if word:
        if command == '':
            command = shell.prevcommands[-1]
        # remove special chars
        new = ''
        options = ''
        for char in word:
            if char not in "eghqrtx&":
                new += char
            else:
                if char == 'p':
                    execute = False
                options += char
        subs = []
        substitutesplit = re.split(subparse, new)
        # magic number from spacing in search (text, sep, find, replace, text, ...)
        word = ''.join(substitutesplit[::4])

        if word[0] in "$^*":
            slicer = d[word[0]]()
        elif '-' in word:
            split = [int(x) if x.isdigit() else None for x in word.split('-')]
            if split[0] is None:
                split[0] = 0
            slicer = d['-'](split[0], split[1])
        else:
            slicer = int(word)
    else:
        slicer = slice(None)
    return command.split()[slicer], execute

def bang_replacement(shell, listing):
    # http://www.softpanorama.org/Scripting/Shellorama/bash_command_history_reuse.shtml
    '''
    n           line n
    -n          n lines back
    !           last command
    bla         last bla command
    ?bla        last use of bla in command

    If the word designator begins with $, %, ^, *, or - the : is not needed.
    :0          command name
    :^          first arg of command    
    :n          arg n of command
    :$          last arg of command
    :*          all the args of command
    :x-y        all args x through y. x=0

    e           remove all but the suffix of a filename
    g           make changes globally, use with s modifier, below
    h           remove the last part of a filename, leaving the "head"
    p           print the command but do not execute it
    q           quote the generated text
    r           remove the last suffix of a filename
    s/old/new/  substitute new for old in the text. Any delimiter may be used. An & in the argument means the value of old. With empty old , use last old , or the most recent !? str ? search if there was no previous old
    t           remove all but the last part of a filename, leaving the "tail"
    x           quote the generated text, but break into words at blanks and newline
    &           repeat the last substitution

    '''
    bang = []
    execute = True
    for part in listing:
        if not part.startswith('"') and not part.startswith("'") and '!' in part:
            for x in re.split(bangparse, part):
                y = True
                if x.startswith("!") and x != '!':
                    x, y = get_hist(shell, x[1:])
                    bang.extend(x)
                elif x:
                    bang.append(x)
                if not y:
                    execute = False
        else:
            bang.append(part)
    if bang != listing:
        shell.stdout.write(' '.join(bang))
    return bang, execute

def filename_expansion(shell, listing):
    filenames = []
    for part in listing:
        if '*' in part or '?' in part or ('[' in part and ']' in part):
            filenames.extend(fs.list_glob(shell.sabs_path(part)))
        else:
            filenames.append(part)
    return filenames

def shell_expansion(shell, string):
    # http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_03_04.html
    quote = quote_split(string)

    # replace bang
    if shell.prevcommands:
        bang, execute = bang_replacement(shell, quote)
    else:
        bang = quote
        execute = True

    #replace $vars
    cleaned = [re.sub(varparse, shell.get_var, xs) for xs in bang]
    filenames = filename_expansion(shell, cleaned)
    return filenames, ' '.join(bang)

def eval_input(shell, cleaned):
    b = [[None, [], None, None]]
    state = None
    charstates = [APPENDCHAR, OUTCHAR, INCHAR, PIPECHAR]
    for part in cleaned:
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
    connect_shells(proper)
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
