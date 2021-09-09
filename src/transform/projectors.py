from .nodeset import flatten_node_sets
from .types import Matcher, TreeNode, NodeSet, Projector, IterableNodeSet


def project_children(node: TreeNode) -> NodeSet:
    return list(node[1:])


class Children(Projector):
    def project(self, node: TreeNode) -> NodeSet:
        return project_children(node)


class DeepDive(Projector):
    """ Find deepest children isolated by non-matching nodes """
    def __init__(self, matcher: Matcher):
        self.matcher = matcher

    def project(self, tree: TreeNode) -> IterableNodeSet:
        def go_deep(node):
            deeper_nodes = list(self.project(node))
            return deeper_nodes if len(deeper_nodes) else [node]

        filtered = filter(
            lambda node: self.matcher.is_match(node),
            project_children(tree)
        )
        node_sets = map(go_deep, filtered)
        return flatten_node_sets(node_sets)
