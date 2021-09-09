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
