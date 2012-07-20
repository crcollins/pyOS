import argparse

class Parser(argparse.ArgumentParser):
    def __init__(self, program, name=None, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, prog=program, *args, **kwargs)
        if name is None:
            self.name = program
        else:
            self.name = name
        self.help = False

    def add_shell(self, shell):
        self.shell = shell

    def exit(self, *args, **kwargs):
        pass

    def print_usage(self, *args, **kwargs):
        try:
            self.shell.stderr.write(self.format_usage())
            self.help = True
        except AttributeError:
            pass

    def print_help(self, *args, **kwargs):
        try:
            self.shell.stdout.write(self.help_msg())
            self.help = True
        except AttributeError:
            pass

    def help_msg(self):
        return "%s\n\n%s" % (self.name, self.format_help())

def calc_permission_string(number):
    base = 'rwxrwxrwx'
    number = str(number)
    binary = []
    for digit in number[:3]:
        binary.extend([int(y) for y in '{0:03b}'.format(int(digit))])
    return ''.join([b if (a and b) else '-' for a, b in zip(binary, base)])

def calc_permission_number(string):
    numbers = []
    string += '-' * (9 - len(string))
    for group in (string[:3], string[3:6], string[6:9]):
        a = ['1' if x and x not in ["-", "0"] else '0' for x in group]
        numbers.append(int("0b" + ''.join(a), 2))
    return ''.join((str(x) for x in numbers))

def validate_permission(value):
    full = 'rwxrwxrwx'
    assert len(value) == len(full)
    for l, f in zip(value, full):
        assert (l == '-') or (l == f)

def convert_many(start, *args):
    if type(start) not in (list, set, tuple):
        done = [(start, ) + args]
    else:
        done = [(x, ) + args for x in start]
    return done