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
    if max_nodes and tag_nodes:
        print('load_spec: allow either max either tag nodes, not both. Got:',
              list(map(str, kids)), file=sys.stderr)
    if max_nodes:
        return max_nodes[0]
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
    bar = kids.pop()
    if not isinstance_xbar(bar):
        print('load_max: the last argument should be xbar, got:', str(bar))
        return None
    spec = kids[0] if len(kids) else None
    return XMax(spec, bar)


def load_bar(type_: XType,
             kids: list[TreeNode]) -> typing.Union[XBarBase, XBarFrame]:
    xhead = kids[0] if kids else None
    compl = kids[1:]
    if not isinstance(xhead, XHead):
        if kids and kids[0] is not None:
            compl = kids
        xhead = XHead(type_, None)
    cls = XBarBase if len(compl) < 2 else XBarFrame
    return cls(xhead, *compl)


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
    kids = map(lexp_to_tree, le[1:])
    if head.endswith('-BAR'):
        type_ = prefix_to_type(head)
        return load_bar(type_, list(kids))
    if head.endswith('-SPEC'):
        return load_spec(list(kids))
    if head.endswith('-MAX'):
        try:
            kids = list(kids)
            return load_max(kids)
        except TypeError as e:
            print('load-rec: bad input to X-MAX:',
                  head, list(map(str, kids)), file=sys.stderr)
            raise e
    return [head, *kids]
