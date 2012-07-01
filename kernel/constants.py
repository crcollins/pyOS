import os

OSNAME = "pyOS"

#The start of the virtual filesystem
BASEPATH = os.getcwd()

#Standard system paths
BASEDIR = "/"
CURRENTDIR = "."
PARENTDIR = ".."
PROGRAMSDIR = "/programs"
KERNELDIR = "/kernel"
METADIR = "/meta"  # need to implement
USERDIR = "/user"  # need to implement
SYSDATADIR = "/data"

#Standard file paths
METADATAFILE = os.path.join(BASEPATH, "data/data")

#Special Characters/strings
VARCHAR = "$"
PATHCHAR = "/"
PIPECHAR = "|"
OUTCHAR = ">"
APPENDCHAR = ">>"
INCHAR = "<"

#System State Vars
REBOOT = -2
SHUTDOWN = -1
IDLE = 0
RUNNING = 1

#Development Vars
IGNORREFILES = [".pyc", ".git"]
