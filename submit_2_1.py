import os
from argparse import ArgumentParser as AP

# Useful addresses
SHIFT_ADDR = "0x401292"
SHIFT_PLUS_ADDR = "0x401286"
CORRECT_ADDR = "0x401211"
CORRECT_PWD = "0x4012a8"
LARGER_ADDR = "0x40126f"
# Path to output folder
OUTPATH = "/home/isl/t2_1/output"

# Returns a string
def sChar(char, offset, is_larger):
    if is_larger:
        newOrd = ord(char) + offset - ord("a")
        newOrd = ord("a") + (newOrd % 26)
    else:
        newOrd = ord(char) + offset

    return chr(newOrd)


# Returns None, since it writes to a file
def main(path_to_traces, out_id):
    traces = os.listdir(path_to_traces)
    pwd_chars = {}
    correct = False

    for t in traces:
        # For debugging purposes
        # print("trace: ", t)
        correct_count = 0
        t = 0
        offset = 0
        is_larger = False
        path = "{}/{}".format(path_to_traces, t)

        for line in open(path, "r").readlines():
            if SHIFT_ADDR in line:
                if offset > 0:
                    pwd_chars[t] = sChar(t[t - 1], offset - 1, is_larger)
                # Reset shift amount and larger guess
                t += 1
                offset = 0
                is_larger = False

            if CORRECT_ADDR in line:
                correct_count += 1
                pwd_chars[t] = t[t - 1]
            if LARGER_ADDR in line:
                is_larger = True
            if SHIFT_PLUS_ADDR in line:
                offset += 1
            if CORRECT_PWD in line:
                correct = True

    correct = True
    # Recover password
    recovered = ""
    for j in range(sorted(pwd_chars.keys())[-1]):
        if j not in pwd_chars.keys():
            recovered = recovered + "_"
            correct = False
        else:
            recovered = recovered + pwd_chars[j]

    if correct:
        recovered += ",complete"
    else:
        recovered += ",partial"

    os.makedirs(OUTPATH, exist_ok=True)
    output = "{}/oput_{}".format(OUTPATH, out_id)
    with open(output) as f:
        f.write(recovered)


if __name__ == "__main__":
    arg_parser = AP()
    arg_parser.add_argument("path")
    arg_parser.add_argument("out_id")
    args = arg_parser.parse_args()
    main(args.paths, args.out_id)