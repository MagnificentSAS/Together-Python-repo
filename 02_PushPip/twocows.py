import argparse
import os
import random
import sys

from cowsay import cowsay, Option, list_cows, read_dot_cow

parser = argparse.ArgumentParser(
    prog=os.path.basename(sys.argv[0]),
    description="Generates an ASCII image of a cow saying the given text",
)

parser.add_argument(
    "-e",
    type=str,
    help="An eye string for 1st cow. This is ignored if a preset mode is given",
    dest="eyes1",
    default=Option.eyes,
    metavar="eye_string1",
)
parser.add_argument(
    "-E",
    type=str,
    help="An eye string 2nd cow. This is ignored if a preset mode is given",
    dest="eyes2",
    default=Option.eyes,
    metavar="eye_string2",
)

parser.add_argument(
    "-f", type=str, metavar="cowfile1",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile1 (if provided as a path, the path must "
         "contain at least one path separator)",
)
parser.add_argument(
    "-F", type=str, metavar="cowfile2",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile2 (if provided as a path, the path must "
         "contain at least one path separator)",
)

parser.add_argument(
    "-l", action="store_true",
    help="Lists all cows in the cow path and exits"
)
parser.add_argument(
    "-n", action="store_false",
    help="If given, text in the speech bubble of 1st cow will not be wrapped"
)
parser.add_argument(
    "-N", action="store_false",
    help="If given, text in the speech bubble of 2nd cow will not be wrapped"
)
parser.add_argument(
    "-T1", type=str, dest="tongue1",
    help="A 1st tongue string. This is ignored if a preset mode is given",
    default=Option.tongue, metavar="tongue_string"
)
parser.add_argument(
    "-T2", type=str, dest="tongue2",
    help="A 2nd tongue string. This is ignored if a preset mode is given",
    default=Option.tongue, metavar="tongue_string"
)

parser.add_argument(
    "-W", type=int, default=40, dest="width", metavar="column",
    help="Width in characters to wrap the speech bubble for both cows (default 40)",
)

group = parser.add_argument_group(
    title="Mode",
    description="There are several out of the box modes "
                "which change the appearance of the cow. "
                "If multiple modes are given, the one furthest "
                "down this list is selected for both cows"
)
group.add_argument("-b", action="store_const", const="b", help="Borg")
group.add_argument("-d", action="store_const", const="d", help="dead")
group.add_argument("-g", action="store_const", const="g", help="greedy")
group.add_argument("-p", action="store_const", const="p", help="paranoid")
group.add_argument("-s", action="store_const", const="s", help="stoned")
group.add_argument("-t", action="store_const", const="t", help="tired")
group.add_argument("-w", action="store_const", const="w", help="wired")
group.add_argument("-y", action="store_const", const="y", help="young")

parser.add_argument(
    "--random", action="store_true",
    help="If provided, picks a random cow from the COWPATH. "
         "Is superseded by the -f option",
)

parser.add_argument(
    "message1", default=None, nargs='?',
    help="The message to include in the speech bubble. "
         "If not given, stdin is used instead."
)

parser.add_argument(
    "message2", default=None, nargs='?',
    help="The message to include in the speech bubble. "
         "If not given, stdin is used instead."
)


def get_cowfile(cow):
    if cow is not None and len(cow.split(os.sep)) > 1:
        with open(cow, "r") as f:
            return read_dot_cow(f)
    else:
        return None


def get_preset(args):
    return (
            args.y or args.w or args.t or args.s
            or args.p or args.g or args.d or args.b
    )

args = parser.parse_args()

if args.l:
    print("\n".join(list_cows()))
    exit(0)

if args.message1 is None:
    args.message1 = sys.stdin.readline()
    args.message2 = sys.stdin.readline()
elif args.message2 is None:
    args.message2 = sys.stdin.read()

if args.random:
    cow1 = args.f or random.choice(list_cows())
    cow2 = args.F or random.choice(list_cows())
else:
    cow1 = args.f or "default"
    cow2 = args.F or "default"

cow_lines1 = cowsay(
    message=args.message1,
    cow=cow1,
    preset=get_preset(args),
    eyes=args.eyes1,
    tongue=args.tongue1,
    width=args.width,
    wrap_text=args.n,
    cowfile=get_cowfile(args.f),
).split('\n')

cow_lines2 = cowsay(
    message=args.message2,
    cow=cow2,
    preset=get_preset(args),
    eyes=args.eyes2,
    tongue=args.tongue2,
    width=args.width,
    wrap_text=args.N,
    cowfile=get_cowfile(args.F),
).split('\n')

max_len1 = 0
for line in cow_lines1:
    new_len = len(line)
    max_len1 = new_len if new_len > max_len1 else max_len1

cow_lines1_free_lines = " " * max_len1

for i in range(len(cow_lines1)):
    cow_lines1[i] += " " * (max_len1 - len(cow_lines1[i]))

cow_lines1 = [cow_lines1_free_lines] * max(len(cow_lines2) - len(cow_lines1), 0) + cow_lines1
cow_lines2 = [""] * max(len(cow_lines1) - len(cow_lines2), 0) + cow_lines2

cow_lines = []
for line1, line2 in zip(cow_lines1, cow_lines2):
    cow_lines.append(line1 + line2)

print("\n".join(cow_lines))