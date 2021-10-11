from .nodeset import flatten_node_sets, is_node, is_node_set,\
    normalize_level, normalize_node
from .types import Matcher, TreeNode, NodeSet, Projector, IterableNodeSet


def project_children(node: TreeNode) -> NodeSet:
    if is_node(node):
        return node[1:]
    if is_node_set(node):  # for headless trees
        return node
    return []


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

        tree = normalize_node(tree)
        if not tree:
            return []

        filtered = filter(
            lambda node: self.matcher.is_match(node),
            normalize_level(project_children(tree))
        )
        node_sets = map(go_deep, filtered)
        return flatten_node_sets(node_sets)
