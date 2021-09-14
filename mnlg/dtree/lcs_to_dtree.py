import typing

from .types import Rule
from ..transform import TreeNode
from ..xbar import XMax


def find_rule(rules: list[Rule], xmax: XMax) -> typing.Optional[Rule]:
    type_ = xmax.type
    head = xmax.xbar.head.s
    return next((rule for rule in rules if rule.x == type_ and rule.head == head), None)


def lcs_to_dtree(rules: list[Rule], lcs: XMax) -> TreeNode:
    rule = find_rule(rules, lcs)
    # TODO FIXME check for None
    return rule.tree
