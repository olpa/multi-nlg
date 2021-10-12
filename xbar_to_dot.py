import argparse
import sys

import typing

from mnlg.xbar.types import XBarBase, XSpecTag, XMax, XSpec, XHead, str_tag
from mnlg.xbar.types import isinstance_xspec, XBarFrame, XBarRec
from mnlg.xbar import lexp


def get_indent(level: int) -> str:
    return '  ' * level


def write_node(h: typing.TextIO,
               label: str,
               level: int,
               id_: str,
               parent_id: typing.Union[str, None]) -> None:
    label = label.replace('"', "'")
    indent = get_indent(level)
    h.write(f'{indent}{id_} [label="{label}"]\n')
    if parent_id:
        h.write(f'{indent}{parent_id} -> {id_}\n')


def to_graphviz_unknown(h: typing.TextIO,
                        node: object,
                        level: int,
                        parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(node)}'
    label = str(node)[:16]
    if len(label) > 16:
        label = label[:13] + '...'
    indent = get_indent(level)
    h.write(f'{indent}{id_} [label="{label}"]\n')
    if parent_id:
        h.write(f'{indent}{parent_id} -> {id_}\n')


def str_tags_iter(tags: typing.Optional[dict[str, str]]) \
        -> typing.Iterable[str]:
    if not tags:
        return []
    return map(str_tag, tags.items())


def to_graphviz_xhead(h: typing.TextIO,
                      xhead: XHead,
                      level: int,
                      parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xhead)}'
    ls = []
    if xhead.s is not None:
        ls.append(xhead.s)
    ls.extend(str_tags_iter(xhead.tags))
    if not ls:
        return
    ls = map(str, ls)
    label = '\\n'.join(ls)
    write_node(h, label, level, id_, parent_id)


def to_graphviz_xbar_base(h: typing.TextIO,
                          xbar: typing.Union[XBarBase, XBarFrame],
                          level: int,
                          parent_id: typing.Union[str, None]) -> None:
    id_ = str(id(xbar))
    write_node(h, str(xbar.type) + "'", level, id_, parent_id)
    if isinstance(xbar.head, XHead):
        to_graphviz_xhead(h, xbar.head, level + 1, id_)
    else:
        to_graphviz_unknown(h, xbar.head, level + 1, id_)
    ls = xbar.compl if isinstance(xbar, XBarFrame) else [xbar.compl]
    for compl in ls:
        if isinstance(compl, XMax):
            to_graphviz_xmax(h, compl, level + 1, id_)
        elif xbar.compl:
            to_graphviz_unknown(h, compl, level + 1, id_)


def to_graphviz_xbar_rec(h: typing.TextIO,
                         xbar: XBarRec,
                         level: int,
                         parent_id: typing.Union[str, None]) -> None:
    id_ = str(id(xbar))
    write_node(h, str(xbar.type) + "'", level, id_, parent_id)
    to_graphviz_xbar(h, xbar.bar, level + 1, id_)
    if isinstance(xbar.adj, XMax):
        to_graphviz_xmax(h, xbar.adj, level + 1, id_)
    else:
        to_graphviz_unknown(h, xbar.adj, level + 1, id_)


def to_graphviz_xbar(h: typing.TextIO,
                     xbar: typing.Union[XBarBase, XBarFrame, XBarRec],
                     level: int,
                     parent_id: typing.Union[str, None]) -> None:
    if isinstance(xbar, XBarBase) or isinstance(xbar, XBarFrame):
        to_graphviz_xbar_base(h, xbar, level, parent_id)
    elif isinstance(xbar, XBarRec):
        to_graphviz_xbar_rec(h, xbar, level, parent_id)
    else:
        to_graphviz_unknown(h, xbar, level, str(id(xbar)))


def to_graphviz_xspec(h: typing.TextIO,
                      xspec: XSpec,
                      level: int,
                      parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xspec)}'
    if isinstance(xspec, XMax):
        return to_graphviz_xmax(h, xspec, level, parent_id)
    if not isinstance(xspec, XSpecTag):
        raise ValueError('Unsupported Spec: ' + str(xspec))
    label = '\n'.join(str_tags_iter(xspec.tags))
    if not label:
        return
    write_node(h, label, level, id_, parent_id)


def to_graphviz_xmax(h: typing.TextIO,
                     xmax: XMax,
                     level: int,
                     parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xmax)}'
    write_node(h, str(xmax.type) + 'P', level, id_, parent_id)
    if isinstance_xspec(xmax.spec):
        to_graphviz_xspec(h, xmax.spec, level + 1, id_)
    elif xmax.spec is not None:
        to_graphviz_unknown(h, xmax.spec, level + 1, id_)
    to_graphviz_xbar(h, xmax.xbar, level + 1, id_)


def to_graphviz(h: typing.TextIO, xmax: XMax) -> None:
    h.write('digraph D {\n')
    if isinstance(xmax, XMax):
        to_graphviz_xmax(h, xmax, 0, None)
    else:
        to_graphviz_unknown(h, xmax, 0, None)
    h.write('}\n')


def parse_command_line():
    parser = argparse.ArgumentParser(description='Visualize XBar tree')
    parser.add_argument('--in',
                        dest='input',
                        help='read the l-expression from the file',
                        metavar='FILE')
    parser.add_argument('--out',
                        dest='output',
                        help='write the graphviz code to the file',
                        metavar='FILE')
    parser.add_argument('rest', nargs='*')
    return parser.parse_args()


def read_input(args):
    import json
    h = None
    s_in = ' '.join(args.rest)
    if args.input:
        h = open(args.input)
    if h is None and not s_in:
        h = sys.stdin
    if h:
        s_in = h.read()
    if h and h is not sys.stdin:
        h.close()

    le = json.loads(s_in)
    return lexp.lexp_to_tree(le)


def main():
    import sys
    args = parse_command_line()
    xmax = read_input(args)
    h = sys.stdout
    if args.output:
        h = open(args.output, 'w')
    try:
        to_graphviz(h, xmax)
    finally:
        if h is not sys.stdout:
            h.close()


if '__main__' == __name__:
    main()
