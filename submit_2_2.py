from argparse import ArgumentParser as AP
import os
import string
from subprocess import Popen, DEVNULL

LOOP_ADDR = "0x401d62"
TRUE_COMP = "0x401d83"

CHARS = list(string.ascii_lowercase)
PW_CHARS = dict()

PATH_TO_SGX = (
    "/home/isl/pin-3.11-97998-g7ecce2dac-gcc-linux-master/source/tools/SGXTrace"
)
PATH_TO_PIN = "/home/isl/pin-3.11-97998-g7ecce2dac-gcc-linux-master/pin"

PATH_TO_BINARY = "/home/isl/t2_2/password_checker_2"
PATH_TO_TRACES = "/home/isl/t2_2/traces"
PATH_TO_OUTPUT = "/home/isl/t2_2/output"


def gen_trace_for_char(char, guess):
    output = "{}/trace_{}".format(PATH_TO_TRACES, char)
    cmd = "{} -t {}/obj-intel64/SGXTrace.so -o {} -trace 1 -- {} {}".format(
        PATH_TO_PIN, PATH_TO_SGX, output, PATH_TO_BINARY, guess
    )
    # os.system(cmd)
    Popen(args=cmd, stdout=DEVNULL, stderr=DEVNULL, shell=True).wait()


def inspect_trace(pwd_chars, char):
    name = "{}/trace_{}".format(PATH_TO_TRACES, char)
    char_pos = 0

    for l in open(name).readlines():
        if LOOP_ADDR in l:
            char_pos += 1
        if TRUE_COMP in l:
            pwd_chars[char_pos] = char

    print("Done with {}".format(char))


def main(out_id):
    for char in CHARS:
        gen_trace_for_char(char, char * 31)
        inspect_trace(PW_CHARS, char)

    recovered = ""
    for pos in range(sorted(PW_CHARS.keys())[-1]):
        recovered = recovered + PW_CHARS[1 + pos]
    recovered = recovered + ",complete"

    output_path = "{}/oput_{}".format(PATH_TO_OUTPUT, out_id)
    with open(output_path, "w") as f:
        f.write(recovered)


if __name__ == "__main__":
    os.makedirs(PATH_TO_OUTPUT, exist_ok=True)
    os.makedirs(PATH_TO_TRACES, exist_ok=True)

    arg_parser = AP()
    arg_parser.add_argument("out_id")
    args = arg_parser.parse_args()
    id = args.out_id
    main(id)
