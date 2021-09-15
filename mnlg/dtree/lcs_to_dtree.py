import typing

from .rules_rgl import to_complement, to_spec, to_x1
from .types import Rule
from ..transform import TreeNode
from ..xbar import XMax


def find_rule(rules: list[Rule], xmax: XMax) -> typing.Optional[Rule]:
    type_ = xmax.type
    xhead = xmax.to_head()
    head = (xhead and xhead.s) or None
    if '???' == head:
        head = None
    return next((rule for rule in rules if rule.x == type_ and rule.head == head), None)


def eval_var(rules: list[Rule],
             lcs: XMax,
             var_expansion: typing.Union[str, typing.Callable[[TreeNode], TreeNode]]
             ) -> typing.Optional[TreeNode]:
    func = var_expansion
    if isinstance(func, str):
        if func == '#complement':
            func = to_complement
        elif func == 'spec':
            func = to_spec
        elif func == 'x1':
            func = to_x1
        else:
            func = lambda _: ['TODO']
    val = func(lcs)
    if (isinstance(val, list) or isinstance(val, tuple)) and len(val):
        if val[0] == 'none':
            val = None
        elif val[0] == 'map':
            val = lcs_to_dtree(rules, val[1])
        elif val[0] == 'mapls':
            val = list(map(
                lambda node: lcs_to_dtree(rules, node),
                val[1]
            ))
    return val


def subst_vars(rules: list[Rule], lcs: XMax, tree: TreeNode, variables: dict[str, TreeNode]) -> TreeNode:
    def level_to_iter(level: list[TreeNode]) -> typing.Iterable[TreeNode]:
        level = iter(level)
        try:
            while True:
                el = next(level)
                if el == '#,':
                    var_name = next(level)
                    val = eval_var(rules, lcs, variables.get(var_name, var_name) if variables else var_name)
                    if val is not None:
                        yield val
                elif el == '#,@':
                    var_name = next(level)
                    val = eval_var(rules, lcs, variables.get(var_name, var_name) if variables else var_name)
                    if val is not None:
                        yield from val
                else:
                    yield el
        except StopIteration:
            pass

    def copy_or_deep(node: TreeNode) -> TreeNode:
        if isinstance(node, list):
            return subst_rec(node)
        else:
            return node

    def subst_rec(node: TreeNode) -> TreeNode:
        return list(map(copy_or_deep, level_to_iter(node)))

    return subst_rec(tree)


def lcs_to_dtree(rules: list[Rule], lcs: XMax) -> TreeNode:
    rule = find_rule(rules, lcs)
    if rule is None:
        # TODO FIXME handle None
        return []
    return subst_vars(rules, lcs, rule.tree, rule.vars)
