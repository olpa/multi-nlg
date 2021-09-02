#!/usr/bin/python3
import re


fname = "manually-parsed-interlingua.txt"

subst = {}


def expand_line(line, subst):
    while True:
        l_orig = line
        for (k, v) in subst.items():
            rexp = re.compile(r'\b{}'.format(k))
            line = rexp.sub(repl=v, string=line)
        if line == l_orig:
            break
    return line


with open(fname) as h:
    for line in h:
        if line.startswith('--'):
            continue
        line = line.strip()
        if not line:
            continue
        if line.startswith('let'):
            (let, token, eq, sub) = line.split(' ', 3)
            subst[token] = sub
            continue
        print(expand_line(line, subst))
