import json
import os
import sys
from json import JSONDecodeError
from typing import Mapping


def load_file(file_name: str) -> Mapping[str, object]:
    parses = {}
    path_to_fixture = os.path.join(os.path.dirname(__file__), '..', 'fixture')
    f = os.path.join(path_to_fixture, file_name)
    with open(f) as h:
        for line in h:
            if '=' not in line:
                continue
            (id_, obj) = line.split('=', 2)
            try:
                parse = json.loads(obj)
                parses[id_.strip()] = parse
            except JSONDecodeError:
                print(
                    'fixture.load_file: can not load as json: >>%s<<' % obj,
                    file=sys.stderr)
    return parses


def load_camxes_parses() -> Mapping[str, object]:
    return load_file('camxes_parse.txt')


def load_lcs() -> Mapping[str, object]:
    return load_file('lcs.txt')
