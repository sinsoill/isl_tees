import os
import subprocess
from time import sleep

PATH = "/home/isl/t1"

COMMAND = 'set variable input="<mes><action type=\\"key-update\\"/></mes>"\n'

def gdb_cmd_exec(p,cmd):
    p.stdin.write(cmd.encode())
    p.stdin.flush()
    sleep(3)
    

def reset():
    os.system("{}/run.sh".format(PATH))
    os.system("kill -9 $(lsof -t -i:5111)")

def init_gdb():
    
    SP = subprocess.Popen(["gdb","python3"], stdin=subprocess.PIPE)
    gdb_cmd_exec(SP,"set breakpoint pending on\n")
    return SP

def task1():
    reset()
    SP = init_gdb()
    sleep(1)
    gdb_cmd_exec(SP, "break gcm_crypt_and_tag\n")
    gdb_cmd_exec(SP,"run sp_server.py\n")
    subprocess.Popen(["sh",f"{PATH}/start.sh"])
    sleep(3)
    gdb_cmd_exec(SP,"c\n")
    gdb_cmd_exec(SP,COMMAND)
    gdb_cmd_exec(SP,"c\n")
    

if __name__ == "__main__":
    os.chdir(PATH)
    task1()
