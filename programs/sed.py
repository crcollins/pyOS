import re

from kernel.utils import Parser
import kernel.filesystem

desc = "Allows editing streams."
parser = Parser('sed', name="Stream Editor", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-e', action="append", type=str, dest="expression")
pa('-f', action="store", type=str, nargs='*', dest="file", default='')
pa('-s', action="store_true", dest="separate", default=False)
pa('-v', action="store_true", dest="invert", default=False)
pa('-i', action="store_true", dest="inplace", default=False)
pa('-n', action="store_true", dest="silent", default=False)


subparse = re.compile(r"""(s)(?P<lim>.)(.*?)(?P=lim)(.*?)(?P=lim)(.*)""")

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            for path in args.paths:
                sed(shell, args, path)
            if not shell.stdout:
                shell.stdout.write('')
        else:
            shell.stderr.write("no stream")

def sed(shell, args, path):
    newpath = shell.sabs_path(path)
    if kernel.filesystem.is_file(newpath):
        if args.inplace:
            out = kernel.filesystem.open_file(newpath + "~", 'w')
        else:
            out = shell.stdout
        with kernel.filesystem.open_file(newpath, 'r') as f:
            try:
                address, command = parse_expression(args.expression[0])
                singleregex = (address[0] == address[-1]) and \
                                (type(address[-1]) == str)
                start = False
                end = False
                linematch = False
                for i, line in enumerate(f):
                    if match(i, line, address[0]):
                        start = True
                    if (start and not end) != command.startswith("!"):
                        line = edit_line(line, command)
                        linematch = True
                    if not args.inplace:
                        line = line.rstrip('\n')
                    if not linematch and args.silent:
                        pass
                    else:
                        out.write(line)
                    if match(i, line, address[-1]):
                        end = True

                    # do resets
                    linematch = False
                    if singleregex:
                        start = False
                        end = False

                if args.inplace:
                    out.close()
                    kernel.filesystem.move(newpath + "~", newpath)
            except:
                shell.stderr.write("No command")
    else:
        shell.stderr.write("%s does not exist" % (newpath, ))

def match(i, line, address):
    if type(address) == int:
        val = i >= address
    else:
        val = bool(re.findall(address, line))
    return val

def edit_line(line, expression):
    try:
        command, sep, regex, repl, flags = re.findall(subparse, expression)[0]
        if command == 's':
            newline = ''
            idx = 0
            for m in re.finditer(regex, line):
                r = repl.replace('&', m.group(0))
                newline += line[idx:m.start()] + r
                idx = m.end()
            newline += line[idx:]
        else:
            newline = line
    except:
        newline = line
    return newline

def parse_expression(expression):
    commands = "qdpnsy!"
    split = re.split("""((?<!\\\\)/.*(?<!\\\\)/)""", expression)
    idx = None
    # separate the groupings
    for i, group in enumerate(split):
        if not group.startswith('/') and any(x in group for x in commands):
            idx = i
            break

    addrstr = ''.join(split[:idx])
    cmdstr = ''
    end = 0
    # separate the induvidual chars
    for letter in ''.join(split[idx:]):
        if not end:
            if letter not in commands:
                addrstr += letter
            else:
                end = 1
                cmdstr += letter
        else:
            cmdstr += letter

    address = addrstr.split(',')
    # clean address values
    for i, value in enumerate(address):
        try:
            address[i] = int(value) - 1
        except:
            # remove the slashes
            address[i] = value[1:-1]
    command = cmdstr
    return address, command

def help():
    return parser.help_msg()

'''
http://www.gnu.org/software/sed/manual/sed.html
http://www.ibm.com/developerworks/linux/library/l-sed1/index.html
Address ranges
==============
first part of line
[start,end]
/regex/command
/[beginregex]/,/[endregex]/command
!
\d*(?<,)\d*


Commands
========
#comment
q [exit code]       quit at end of pattern space
d                   delete the pattern space
p                   print out pattern
n                   print pattern space and insert next line
{ commands }        group of commands
s                   s/regex/replacement/flags
    replacement
        \L          turn replacement lowercase until \U or \E
        \l          turn the next char lowercase
        \U          turn replacement uppercase until \L or \E
        \u          turn the next char to uppercase
        \E          Stop case conversion
        \[n]        number of inclusions
        &           matched pattern
    flags
        g           apply replacement to all matches
        [num]       only replace the /num/th match
        p           if sub was made, print pattern space
        w [file]    if sub was made, write result to file
                    this incudes /dev/stdout/ and /dev/stderr/
        i/I         case insensitive match
        m/M         multiline?
y                   /source-chars/dest-chars/
'''