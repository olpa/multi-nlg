from .apply_templates import apply_templates_iter
from .projectors import project_children
from .nodeset import is_node, flatten_node_sets, is_node_set
from .types import TreeNode, Transformer, Rule, NodeSet, IterableNodeSet


class Replace(Transformer):
    """ Replace with a constant tree """
    def __init__(self, replacement: NodeSet):
        if not is_node_set(replacement):
            raise ValueError('Should replace with a node set')
        self.replacement = replacement

    def transform(self, _1: list['Rule'], _2: TreeNode) -> NodeSet:
        return self.replacement


class TransformChildren(Transformer):
    """ Ignore the context node, transform its children """
    def transform(self,
                  rules: list['Rule'],
                  node: TreeNode) -> IterableNodeSet:
        if not is_node(node):
            return []

        node_sets = map(
            lambda kid_node: apply_templates_iter(rules, kid_node),
            project_children(node)
        )
        return flatten_node_sets(node_sets)


class TransformCopy(Transformer):
    """ Copy the context node and transform its children """
    helper = TransformChildren()

    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        if not is_node(node):
            return [node]
        node_name: str = node[0]
        return [[
            node_name,
            *self.helper.transform(rules, node)
        ]]
