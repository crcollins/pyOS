import time
import random

def run(shell, args):
    for line in shell.stdin.read():
        print(line)
        time.sleep(1*random.random())

def help():
    return ''