import sys
import typing

from ..transform import TreeNode
from .types import XBarFrame, XSpec, XBar, isinstance_xbar
from .types import XBarBase, XType, XSpecTag, XMax, XHead


def cast_to_tag(le: object) -> str:
    if isinstance(le, list) and 2 == len(le) and 'tag' == le[0]:
        return le[1]
    return str(le)


def is_tag_node(le: object) -> bool:
    return isinstance(le, list) \
        and 2 <= len(le) <= 3 \
        and 'tag' == le[0]


def update_tags(tags: dict[str, str], tag_node: list):
    tag_name = tag_node[1]
    tag_value = tag_node[2] if len(tag_node) >= 3 else tag_name
    tags[tag_name] = tag_value


def split_on_tags_and_not(nodes: list[TreeNode])\
        -> typing.Tuple[list[TreeNode], list[object]]:
    oth_nodes = []
    tag_nodes = []
    for node in nodes:
        if is_tag_node(node):
            tag_nodes.append(node)
        else:
            oth_nodes.append(node)
    if len(oth_nodes) > 1:
        print('load_spec: allow at most one max node. Got:',
              list(map(str, oth_nodes)), file=sys.stderr)
    return tag_nodes, oth_nodes


def assert_xmax_p(prefix: str, node: object) -> bool:
    if not isinstance(node, XMax):
        print(prefix, node)
        return False
    return True


def load_head(type_: XType, kids: list[TreeNode]) -> typing.Optional[XHead]:
    if not kids:
        return XHead(type_, None)
    tag_nodes, name_nodes = split_on_tags_and_not(kids)
    name = name_nodes[0] if name_nodes else None
    tags = {}
    for tag_node in tag_nodes:
        update_tags(tags, tag_node)
    if not tags:
        tags = None
    return XHead(type_, name, tags)


def load_spec(kids: typing.Union[list[TreeNode], XMax]) \
        -> typing.Optional[XSpec]:
    if not kids:
        return None
    tag_nodes, max_nodes = split_on_tags_and_not(kids)
    max_nodes = list(filter(
        lambda node: assert_xmax_p('load_spec: should be X-MAX, got:', node),
        max_nodes))
    if max_nodes and tag_nodes:
        print('load_spec: allow either max either tag nodes, not both. Got:',
              list(map(str, kids)), file=sys.stderr)
    if max_nodes:
        return typing.cast(XMax, max_nodes[0])
    if not tag_nodes:
        return None
    tags = {}
    for tag_node in tag_nodes:
        update_tags(tags, tag_node)
    return XSpecTag(tags)


def load_max(kids: list[TreeNode]) -> typing.Optional[XMax]:
    if not(1 <= len(kids) <= 2):
        print('load_max: expected one or two kids, got:', list(map(str, kids)))
        return None
    bar = typing.cast(XBar, kids.pop())
    if not isinstance_xbar(bar):
        print('load_max: the last argument should be xbar, got:', str(bar))
        return None
    spec = kids[0] if len(kids) else None
    return XMax(spec, bar)


def get_head_and_compl(
        type_: XType,
        kids: list[TreeNode]) \
        -> typing.Tuple[typing.Optional[XHead], list[XMax]]:
    xhead = kids[0] if kids else None
    compl = kids[1:]
    if not isinstance(xhead, XHead):
        if kids and kids[0] is not None:
            compl = kids
        xhead = XHead(type_, None)
    compl = list(filter(
        lambda node: assert_xmax_p(
            'get_head_and_compl: complement should be X-MAX, got:', node),
        compl))
    return xhead, typing.cast(list[XMax], compl)


def load_bar(type_: XType,
             kids: list[TreeNode]) -> typing.Union[XBarBase, XBarFrame]:
    xhead, ls_compl = get_head_and_compl(type_, kids)
    if len(ls_compl) > 1:
        print('load_bar: expected at most one complement, got:',
              list(map(str, ls_compl)))
    compl = ls_compl[0] if ls_compl else None
    return XBarBase(xhead, compl)


def load_frame(
        type_: XType,
        kids: list[TreeNode]) -> typing.Union[XBarBase, XBarFrame]:
    xhead, ls_compl = get_head_and_compl(type_, kids)
    return XBarFrame(xhead, *ls_compl)


def prefix_to_type(elem_name):
    letter = elem_name[0]
    return XType[letter]


def lexp_to_tree(le: TreeNode
                 ) -> typing.Union[XMax, XSpec, XHead, XBar, TreeNode, list]:
    if not isinstance(le, list):
        return le
    head = le[0]
    if not isinstance(head, str):
        return le
    if 1 == len(head):
        type_ = prefix_to_type(head)
        return load_head(type_, le[1:])
    kids = list(map(lexp_to_tree, le[1:]))
    if head.endswith('-BAR'):
        type_ = prefix_to_type(head)
        return load_bar(type_, kids)
    if head == 'V-FRAME':
        return load_frame(XType.V, kids)
    if head.endswith('-SPEC'):
        return load_spec(kids)
    if head.endswith('-MAX'):
        try:
            return load_max(kids)
        except TypeError as e:
            print('load-rec: bad input to X-MAX:',
                  head, list(map(str, kids)), file=sys.stderr)
            raise e
    return [head, *kids]