import kernel.filesystem

def run(shell, args):
    if args:
        for x in shell.program_paths(args[0]):
            program = kernel.filesystem.open_program(x)
            if program:
                shell.stdout.write(x)
                break

def help():
    a = """
    Which

    Prints the location of the program to be used.

    usage: which [program]
    """
    return a