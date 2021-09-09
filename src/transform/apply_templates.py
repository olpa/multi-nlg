import typing
from .types import TreeNode, Rule, IterableNodeSet, NodeSet
from .matchers import MatchNode


def select_rule(rules: list[Rule], tree: TreeNode) -> typing.Union[Rule, None]:
    return next(
        filter(
            lambda rule: rule.match.is_match(tree),
            rules
        ),
        default_rule
    )


def apply_templates_iter(rules: list[Rule], tree: TreeNode) -> IterableNodeSet:
    rule = select_rule(rules, tree)
    if not rule:
        return []

    return filter(
        lambda node: node is not None and node is not [],
        rule.transform.transform(rules, tree)
    )


def apply_templates(rules: list[Rule], tree: TreeNode) -> NodeSet:
    return list(apply_templates_iter(rules, tree))


from .transformers import TransformCopy  # noqa E402: essential circual reference
default_rule = Rule(MatchNode(), TransformCopy())
