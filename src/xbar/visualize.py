import optparse

import typing

from xbar import XBarBase, XType, XSpecTag, XMax, XBar, XSpec, XHead


def cast_to_tag(lexp: object) -> str:
    if isinstance(lexp, list) and 2 == len(lexp) and 'tag' == lexp[0]:
        return lexp[1]
    return str(lexp)


def load_head(type_: XType, kids):
    if not kids:
        return XHead(type_, None)
    name = None
    if isinstance(kids[0], str):
        name = kids[0]
        tags = kids[1:]
    else:
        tags = kids
    tags = list(map(cast_to_tag, tags))
    return XHead(type_, name, tags)


def load_rec(lexp):
    if not isinstance(lexp, list):
        return lexp
    head = lexp[0]
    if 'N' == head:
        return load_head(XType.N, lexp[1:])
    if 'V' == head:
        return load_head(XType.V, lexp[1:])
    if 'I' == head:
        return load_head(XType.I, lexp[1:])
    kids = map(load_rec, lexp[1:])
    if head in ('N-BAR', 'V-BAR', 'I-BAR'):
        xhead = next(kids)
        xcompl = next(kids, None)
        return XBarBase(xhead, xcompl)
    if head in ('N-SPEC', 'V-SPEC', 'I-SPEC'):
        kids = list(kids)
        in_spec = next(iter(kids), None)
        if isinstance(in_spec, XMax):
            return in_spec
        tags = list(map(cast_to_tag, kids))
        return XSpecTag(tags)
    if head in ('N-MAX', 'V-MAX', 'I-MAX'):
        kids = list(kids)
        return XMax(*kids)
    return [head, *kids]


def get_indent(level: int) -> str:
    return '  ' * level


def write_node(h: typing.TextIO,
               label: str,
               level: int,
               id_: str,
               parent_id: typing.Union[str, None]) -> None:
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


def to_graphviz_xhead(h: typing.TextIO,
                      xhead: XHead,
                      level: int,
                      parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xhead)}'
    ls = []
    if xhead.s is not None:
        ls.append(xhead.s)
    if xhead.tags:
        ls.append('|'.join(xhead.tags))
    label = '\\n'.join(ls)
    write_node(h, label, level, id_, parent_id)


def to_graphviz_xbar(h: typing.TextIO,
                     xbar: XBar,
                     level: int,
                     parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xbar)}'
    write_node(h, str(xbar.type) + "'", level, id_, parent_id)
    to_graphviz_xhead(h, xbar.head, level + 1, id_)
    if isinstance(xbar.compl, XMax):
        to_graphviz_xmax(h, xbar.compl, level + 1, id_)
    elif xbar.compl:
        to_graphviz_unknown(h, xbar.compl, level + 1, id_)


def to_graphviz_xspec(h: typing.TextIO,
                      xspec: XSpec,
                      level: int,
                      parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xspec)}'
    if isinstance(xspec, XMax):
        return to_graphviz_xmax(h, xspec, level, parent_id)
    if isinstance(xspec, XSpecTag):
        label = '|'.join(xspec.tags)
    else:
        raise ValueError('Unsupported Spec: ' + str(xspec))
    if not label:
        return
    write_node(h, label, level, id_, parent_id)


def to_graphviz_xmax(h: typing.TextIO,
                     xmax: XMax,
                     level: int,
                     parent_id: typing.Union[str, None]) -> None:
    id_ = f'node{id(xmax)}'
    write_node(h, str(xmax.type) + 'P', level, id_, parent_id)
    to_graphviz_xspec(h, xmax.spec, level + 1, id_)
    to_graphviz_xbar(h, xmax.xbar, level + 1, id_)


def to_graphviz(h: typing.TextIO, xmax: XMax) -> None:
    h.write('digraph D {\n')
    to_graphviz_xmax(h, xmax, 0, None)
    h.write('}\n')


def parse_command_line():
    parser = optparse.OptionParser()
    parser.add_option('--in',
                      dest='input',
                      help='read the l-expression from the file',
                      metavar='FILE')
    parser.add_option('--out',
                      dest='output',
                      help='write the graphviz code to the file',
                      metavar='FILE')
    return parser.parse_args()


def read_input(options, args):
    import json
    import sys
    h = None
    s_in = ' '.join(args)
    if options.input:
        h = open(options.input)
    if h is None and not s_in:
        h = sys.stdin
    if h:
        s_in = h.read()
    if h and h is not sys.stdin:
        h.close()

    s_in = s_in.replace("'", '"')
    lexp = json.loads(s_in)
    return load_rec(lexp)


def main():
    import sys
    (options, args) = parse_command_line()
    xmax = read_input(options, args)
    h = sys.stdout
    if options.output:
        h = open(options.output, 'w')
    try:
        to_graphviz(h, xmax)
    finally:
        if h is not sys.stdout:
            h.close()


if '__main__' == __name__:
    main()
