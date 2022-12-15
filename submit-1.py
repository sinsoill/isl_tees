import os
from subprocess import *
import signal
from time import sleep
import re

PATH = "/home/isl/t1"

COMMAND = '"set variable input = "<mes><action val=\"key-update\"/></mes>"'

def gdb_cmd_exec(p,cmd):
    p.stdin.write(cmd.encode())
    p.stdin.flush()

def reset():
    os.system("kill -9 $(lsof -t -i:3500)")
    os.system("kill -9 $(lsof -t -i:4450)")
    os.system("kill -9 $(lsof -t -i:5111)")


def init_gdb() -> Popen:
    
    os.system(f"cd {PATH} && {PATH}run_manager.sh ")
    os.system(f"cd {PATH}  && {PATH}run_peripheral.sh ")

    sleep(2)
    string_parser = Popen(['gdb', '-q', '-x', f'{PATH}sp_server.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    sleep(1)
    gdb_cmd_exec(string_parser,'set pagination off\n')
    gdb_cmd_exec(string_parser,"set follow-fork-mode child\n")
    gdb_cmd_exec(string_parser,"set breakpoint pending on\n")
    sleep(2)
    return string_parser

def task1():
    SP = init_gdb()
    gdb_cmd_exec(SP, "break gcm_crypt_and_tag\n")

    RP = Popen([f"{node_prefix}node", "--no-warnings", f"{path}remote_party"])

def main():
    try:
        task1()
        reset()
    except:
        pass

if __name__ == "__main__":
    reset()
    try:
        main()
    except Exception as e:
        print(e)
        print(f"An error occured in main!")
    finally:
        reset()
    os.system("cd /home/isl/t1 && /home/isl/t1/run.sh")
    print("Exploit done")
    exit()
