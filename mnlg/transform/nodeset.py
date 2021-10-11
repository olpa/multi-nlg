import itertools
import typing
from .types import TreeNode, NodeSet, IterableNodeSet


def is_node(node: typing.Union[TreeNode, NodeSet]) -> bool:
    return isinstance(node, list) and len(node) and isinstance(node[0], str)


def is_node_set(node: typing.Union[TreeNode, NodeSet]) -> bool:
    # `itertools.chain` is used in `flatten_node_sets`
    if isinstance(node, itertools.chain):
        return True
    return isinstance(node, list) and not is_node(node)


def to_node_set(node: typing.Union[TreeNode, NodeSet]) -> NodeSet:
    return node if is_node_set(node) else [node]


def flatten_node_sets(node_sets: typing.Iterable[IterableNodeSet]
                      ) -> IterableNodeSet:
    return itertools.chain.from_iterable(node_sets)


def debug_print(prefix: str, node_set: IterableNodeSet) -> IterableNodeSet:
    bak = list(node_set)
    print(prefix, bak)
    return bak


# Unwrap camxes constructions like [['time', [['time_offset' ... ]]]]
def normalize_level(node: TreeNode) -> typing.Generator[TreeNode, None, None]:
    if is_node(node):
        yield node
        return
    if not is_node_set(node):
        yield node
        return
    for kid in node:
        if is_node_set(kid):
            yield from normalize_level(kid)
        else:
            yield kid


def normalize_node(node: TreeNode) -> typing.Optional[TreeNode]:
    node_after = list(normalize_level(node))
    if len(node_after) != 1:
        print('normalize_node: after normalization, got several nodes.'
              f'before: {node}, after: {node_after}')
        return None
    return node_after[0]
