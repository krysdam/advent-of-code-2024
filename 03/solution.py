import re

# Regexes, and what they save from the match

# mul(x,y) --> ("x", "y")
RE_MUL = r'mul\((\d{1,3}),(\d{1,3})\)'

# do() --> "do"
RE_DO = r'(do)\(\)'
# don't() --> "don't"
RE_DONT = r"(don't)\(\)"

# any of these commands --> ("x", "y", "do", "don't"),
# with nonapplicable values as ""
RE_COMMAND = RE_MUL + '|' + RE_DO + '|' + RE_DONT


def pull_commands(line):
    """Given a line of the file, return the commands.
    
    A command is either "do", "don't",
    or a mul which is represented as (x, y) where x and y are integers
    """
    bare_commands = re.findall(RE_COMMAND, line)
    commands = []
    for x,y,do,dont in bare_commands:
        if x and y:
            commands.append( (int(x), int(y)) )
        elif do:
            commands.append("do")
        elif dont:
            commands.append("don't")
    return commands

def run_commands(cmds, care_about_do):
    """Run the commands. If care_about_do, toggle with do() and don't()."""
    total = 0
    enabled = True
    for cmd in cmds:
        if cmd == "do":
            enabled = True
        elif cmd == "don't":
            if care_about_do:
                enabled = False
        elif enabled:
            total += cmd[0] * cmd[1]
    return total


# Pull all the commands
cmds = []
with open('input.txt') as f:
    for line in f:
        cmds.extend(pull_commands(line))

# Run the commands
print(f"Part 1: {run_commands(cmds, False)}")
print(f"Part 2: {run_commands(cmds, True)}")