import sys
import typing

from ..transform import TreeNode
from .types import XBarFrame, XSpec, XBar, isinstance_xbar, XBarRec
from .types import XBarBase, XType, XSpecTag, XMax, XHead


def is_node_name(node: TreeNode, name: str) -> bool:
    if not isinstance(node, list):
        return False
    if not node:
        return False
    return node[0] == name


def get_node_name(node: TreeNode) -> typing.Optional[str]:
    if not isinstance(node, list):
        return None
    if not node:
        return None
    name = node[0]
    if not isinstance(name, str):
        return None
    return name


def is_max_node(node: TreeNode) -> bool:
    name = get_node_name(node)
    return name and name.endswith('-MAX')


def is_spec_node(node: TreeNode) -> bool:
    name = get_node_name(node)
    return name and name.endswith('-SPEC')


def is_bar_node(node: TreeNode) -> bool:
    name = get_node_name(node)
    return name and (name.endswith('-BAR')
                     or name.endswith('-FRAME')
                     or name.endswith('-BAR-REC'))


def is_head_node(node: TreeNode) -> bool:
    name = get_node_name(node)
    return name and len(name) == 1


def lexp_to_complement(node: TreeNode) -> typing.Optional[TreeNode]:
    """ from X-MAX to the complement """
    if len(node) != 2:
        print('lexp_to_complement: X-MAX should consist of the node name'
              ' and a bar node, got:', node, file=sys.stderr)
        return None
    _, bar_node = node
    while len(bar_node) and is_bar_node(bar_node[0]):
        bar_node = bar_node[0]
    if not is_bar_node(bar_node):
        print('lexp_to_complement: descent to bar-node. Got not a bar node:',
              bar_node, file=sys.stderr)
        return None
    compl_node = bar_node[-1]
    if is_max_node(compl_node):
        return compl_node
    if not is_head_node(compl_node):
        print('lexp_to_complement: the last child of the bar-node should'
              ' be X-MAX or X-HEAD:', bar_node, file=sys.stderr)
    return None


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


def lsstr(ls: list) -> list:
    return list(map(str, ls))


def load_bar(kids: list[TreeNode]) -> typing.Union[XBarBase, XBarRec, None]:
    x_kids = {}
    for x_kid in map(lexp_to_tree, kids):
        cls = type(x_kid)
        if cls in x_kids:
            print(f'load_bar: kids of type {cls}',
                  f'is seen already: {x_kids[cls]}.',
                  f'Dup: {x_kid}, all kids: {lsstr(x_kids)}',
                  file=sys.stderr)
            return None
        x_kids[cls] = x_kid

    if not x_kids or len(x_kids) > 2:
        print('load_bar: expected 1 or 2 children, got:',
              f'{len(x_kids)}, {lsstr(x_kids)}',
              file=sys.stderr)
        return None

    if XHead in x_kids:
        compl = x_kids.get(XMax)
        if compl is None and len(x_kids) == 2:
            print('load_bar: in addition to XHead, expected an XMax,',
                  f'got: {lsstr(x_kids)}',
                  file=sys.stderr)
            return None
        return XBarBase(x_kids[XHead], compl)

    x_bar = (x_kids.get(XBarBase)
             or x_kids.get(XBarFrame)
             or x_kids.get(XBarRec))
    if x_bar:
        if XMax not in x_kids:
            print('load_bar: in addition to XBar, expected an XMax,',
                  f'got: {lsstr(x_kids)}',
                  file=sys.stderr)
        return XBarRec(x_bar, x_kids[XMax])

    print('load_bar: should have XHead or XBar among children,',
          f'got: {lsstr(x_kids)}',
          file=sys.stderr)
    return None


def load_frame(
        type_: XType,
        kids: list[TreeNode]) -> typing.Union[XBarBase, XBarFrame]:
    xhead, ls_compl = get_head_and_compl(type_, kids)
    return XBarFrame(xhead, *ls_compl)


def prefix_to_type(elem_name) -> typing.Optional[str]:
    letter = elem_name[0]
    try:
        return XType[letter]
    except KeyError:
        return None


def lexp_to_tree(le: TreeNode
                 ) -> typing.Union[XMax, XSpec, XHead, XBar, TreeNode, list]:
    if not isinstance(le, list):
        return le
    head = le[0]
    if not isinstance(head, str):
        return le
    if 1 == len(head):
        type_ = prefix_to_type(head)
        if not type_:
            print(f'lexp_to_tree: unknown type: "{type_}"', file=sys.stderr)
            return None
        return load_head(type_, le[1:])
    kids = list(map(lexp_to_tree, le[1:]))
    if head.endswith('-BAR'):
        type_ = prefix_to_type(head)
        return load_bar(kids)
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
