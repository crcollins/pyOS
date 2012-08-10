pyOS
====
pyOS (prounounced "pious") is a python implemention of a psuedo unix-like operating system.

Requirements
-------------
- Python 2.7+

Features
--------
- unix terminal interface
- common utilities (cp, mv, rm, ls, cat, head, sed, etc)
- piping and stdio redirection
- semi virtual filesystem
- file/directory metadata
- dynamic manipulation of files
- basic system call structure
- file/directory permissions
- basic user system

Todo
----
- sdterr redirection
- other utilities (xargs, edit(ed?), awk, etc)
- polish utilities
- formalize the directory structure
- thread(multiprocess?) processes
- exit codes
- tests
- documentation
- formalize syscalls
- networking
- \`command\` execution
- user commands (add, delete, change permissions, etc)

Setup
-----
- cd into the pyOS directory
- run pyOS.py