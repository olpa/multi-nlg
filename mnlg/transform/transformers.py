from __future__ import annotations
from abc import ABC

from .apply_templates import apply_templates_iter
from .projectors import project_children
from .nodeset import is_node_set
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
        return apply_templates_iter(rules, project_children(node))


class TransformCopyBase(Transformer, ABC):
    for_children = TransformChildren()

    def transform_with_first_node(self,
                                  rules: list['Rule'],
                                  node: TreeNode,
                                  first_node: TreeNode) -> IterableNodeSet:
        if is_node_set(node):  # support headless nodes
            return self.for_children.transform(rules, node)
        if isinstance(node, list) and len(node):
            return [[
                first_node,
                *self.for_children.transform(rules, node)
            ]]
        return node


class TransformCopy(TransformCopyBase):
    """ Copy the context node and transform its children """

    def transform(self, rules: list['Rule'],
                  node: TreeNode) -> IterableNodeSet:
        first_node = node[0] if \
            isinstance(node, list) and len(node) else '<ErrTC>'
        return self.transform_with_first_node(rules, node, first_node)


class TransformRename(TransformCopyBase):
    """ Rename the context node and transform its children """

    def __init__(self, new_name: str):
        self.name = new_name

    def transform(self, rules: list['Rule'],
                  node: TreeNode) -> IterableNodeSet:
        first_node = self.name if \
            isinstance(node, list) and len(node) else '<ErrTR>'
        return self.transform_with_first_node(rules, node, first_node)


class Drop(Transformer):
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        return []
