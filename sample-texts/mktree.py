#!/usr/bin/python3

fname = "manually-parsed-interlingua.txt"

subst = {}

def expand_line(l, subst):
    while True:
        l_orig = l
        for (k, v) in subst.items():
            l = l.replace(k, v)
        if l == l_orig:
            break
    return l

with open(fname) as h:
    for l in h:
        if l.startswith('--'):
            continue
        l = l.strip()
        if not l:
            continue
        if l.startswith('let'):
            (let, token, eq, sub) = l.split(' ', 3)
            subst[token] = sub
            continue
        print(expand_line(l, subst))
