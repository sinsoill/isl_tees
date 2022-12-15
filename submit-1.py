import os
from subprocess import *
import signal
from time import sleep
import re

PATH = "/home/isl/t1"

COMMAND = 'set variable input = "<mes><action val=\"key-update\"/></mes>"'

def gdb_cmd_exec(p:Popen,cmd):
    i= p.stdin.write(cmd.encode())
    print(i)
    p.stdin.flush()
    

def reset():
    os.system("kill -9 $(lsof -t -i:5111)")
    os.system("kill -9 $(lsof -t -i:3500)")
    os.system("kill -9 $(lsof -t -i:4450)")

def init_gdb() -> Popen:
    
    os.system(f"cd {PATH} && {PATH}/run_manager.sh ")
    os.system(f"cd {PATH}  && {PATH}/run_peripheral.sh ")

    sleep(2)
    string_parser = Popen(['gdb', 'python3'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    sleep(1)
    gdb_cmd_exec(string_parser,'set pagination off\n')
    gdb_cmd_exec(string_parser,"set follow-fork-mode child\n")
    gdb_cmd_exec(string_parser,"set breakpoint pending on\n")
    return string_parser

def task1():
    SP = init_gdb()
    SP.communicate()
    gdb_cmd_exec(SP, "break gcm_crypt_and_tag\n")
    gdb_cmd_exec(SP, "run sp_server.py\n")
    os.system(f"cd {PATH}  && {PATH}/start.sh")
    sleep(3)
    gdb_cmd_exec(SP, "continue\n")
    sleep(3)
    gdb_cmd_exec(SP, "continue\n")
    sleep(3)
    gdb_cmd_exec(SP, COMMAND+"\n")
    sleep(3)

if __name__ == "__main__":
    reset()
    task1() 


