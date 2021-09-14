import typing
from .nodeset import is_node
from .types import TreeNode, Matcher


class MatchAlways(Matcher):
    def is_match(self, node: TreeNode) -> bool:
        return True


class MatchNode(Matcher):
    def is_match(self, node: TreeNode) -> bool:
        return is_node(node)


class MatchName(Matcher):
    def __init__(self, name: str):
        self.name = name

    def is_match(self, node: TreeNode) -> bool:
        return is_node(node) and node[0] == self.name


class MatchNameCondition(Matcher):
    def __init__(self, predicate: typing.Callable[[str], bool]):
        self.predicate = predicate

    def is_match(self, node: TreeNode) -> bool:
        return is_node(node) and self.predicate(node[0])
