from __future__ import annotations
import typing
from .types import TreeNode, Rule, IterableNodeSet, NodeSet
from .nodeset import to_node_set, flatten_node_sets
from .matchers import MatchNode


def select_rule(rules: list[Rule], tree: TreeNode) -> typing.Union[Rule, None]:
    return next(
        filter(
            lambda rule: rule.match.is_match(tree),
            rules
        ),
        default_rule
    )


def apply_templates_to_node(rules: list[Rule],
                            tree: TreeNode) -> IterableNodeSet:
    rule = select_rule(rules, tree)
    if not rule:
        return []

    return filter(
        lambda node: node is not None and node is not [],
        rule.transform.transform(rules, tree)
    )


def apply_templates_iter(rules: list[Rule],
                         node_set: NodeSet) -> IterableNodeSet:
    return flatten_node_sets(map(
        lambda node: apply_templates_to_node(rules, node),
        node_set
    ))


def apply_templates(rules: list[Rule],
                    tree: typing.Union[TreeNode, NodeSet]) -> NodeSet:
    return list(apply_templates_iter(rules, to_node_set(tree)))


from .transformers import TransformCopy  # noqa E402: essential circual reference
default_rule = Rule(MatchNode(), TransformCopy())
