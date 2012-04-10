import kernel.filesystem

def run(shell, args):
    if len(args) >= 1:
        name = args[0]
        for x in shell.program_paths(name):
            program = kernel.filesystem.open_program(x)
            if program:
                shell.stdout.put(program.help())
                break
        else:
            shell.stderr.put("%s: command not found" %name)
    else:
        shell.stdout.put(help())

def help():
    a = """
    Help

    Returns the help message of the given program.

    usage: help [program]
    """
    return a