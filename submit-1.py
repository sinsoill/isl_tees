from cryptodome import *
import os
import subprocess
import signal
from time import sleep
import re

PATH = "/home/isl/t1"


def gdb_cmd_exec(p,cmd):
    p.stdin.write(cmd.encode())
    p.stdin.flush()
