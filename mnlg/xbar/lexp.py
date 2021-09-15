import sys
import typing

from ..transform import TreeNode
from .types import isinstance_xspec, XBarFrame, XSpec, XBar
from .types import XBarBase, XType, XSpecTag, XMax, XHead


def cast_to_tag(le: object) -> str:
    if isinstance(le, list) and 2 == len(le) and 'tag' == le[0]:
        return le[1]
    return str(le)


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


def prefix_to_type(elem_name):
    letter = elem_name[0]
    return XType[letter]


def lexp_to_tree(le: TreeNode
                 ) -> typing.Union[XMax, XSpec, XHead, XBar, TreeNode, list]:
    if not isinstance(le, list):
        return le
    head = le[0]
    if head in ('N', 'V', 'I'):
        type_ = prefix_to_type(head)
        return load_head(type_, le[1:])
    kids = map(lexp_to_tree, le[1:])
    if head in ('N-BAR', 'V-BAR', 'I-BAR'):
        xhead = next(kids)
        if isinstance(xhead, XHead):
            compl = list(kids)
        else:
            type_ = prefix_to_type(head)
            xhead_rec = xhead
            xhead = XHead(type_, '???')
            if xhead_rec is None:
                compl = list(kids)
            else:
                compl = [xhead, *kids]
        cls = XBarBase if len(compl) < 2 else XBarFrame
        return cls(xhead, *compl)
    if head in ('N-SPEC', 'V-SPEC', 'I-SPEC'):
        kids = list(kids)
        in_spec = next(iter(kids), None)
        if isinstance(in_spec, XMax):
            return in_spec
        tags = list(map(cast_to_tag, kids))
        return XSpecTag(tags)
    if head in ('N-MAX', 'V-MAX', 'I-MAX'):
        kids = list(kids)
        try:
            spec = next(iter(kids), None)
            if isinstance_xspec(spec):
                return XMax(*kids)
            return XMax(None, *kids)
        except TypeError as e:
            print('load-rec: bad input to X-MAX:',
                  head, list(map(str, kids)), file=sys.stderr)
            raise e
    return [head, *kids]
