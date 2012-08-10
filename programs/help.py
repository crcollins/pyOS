def run(shell, args):
    if len(args) >= 1:
        name = args[0]
        for x in shell.program_paths(name):
            program = shell.syscall.open_program(x)
            if program:
                shell.stdout.write(program.help())
                break
        else:
            shell.stderr.write("%s: command not found" % (name, ))
    else:
        shell.stdout.write(help())

def help():
    a = """
    Help

    Returns the help message of the given program.

    usage: help [program]
    """
    return a
