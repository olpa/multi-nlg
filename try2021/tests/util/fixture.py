import json
import os
import sys
from json import JSONDecodeError
from typing import Mapping


def load_string_file(file_name: str) -> Mapping[str, str]:
    path_to_fixture = os.path.join(os.path.dirname(__file__), '..', 'fixture')
    f = os.path.join(path_to_fixture, file_name)
    mapping = {}
    with open(f) as h:
        for line in h:
            if '=' not in line:
                continue
            (id_, s) = line.split('=', 2)
            s = s.strip()
            if s.startswith('$'):
                s = mapping[s[1:]]
            mapping[id_.strip()] = s
    return mapping


def load_file(file_name: str) -> Mapping[str, object]:
    parses = {}
    for id_, s in load_string_file(file_name).items():
        try:
            parse = json.loads(s)
            parses[id_] = parse
        except JSONDecodeError:
            print(
                'fixture.load_file: can not load as json: >>%s<<' % s,
                file=sys.stderr)
    return parses


def load_lcs() -> Mapping[str, object]:
    return load_file('lcs.txt')


def load_dtree() -> Mapping[str, object]:
    return load_file('dtree.txt')


load_stree = load_dtree


def load_gf() -> Mapping[str, str]:
    return load_string_file('gf.txt')
