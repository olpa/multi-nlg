import typing

from .functions import to_complement, to_spec, to_x2, to_x3
from .functions import copy_spec, copy_x2, manner_x3
from .types import Rule
from ..transform import TreeNode
from mnlg.xbar import lexp_to_tree, XMax, XType


def find_rule(rules: list[Rule], xmax: XMax) -> typing.Optional[Rule]:
    type_ = xmax.type
    xhead = xmax.to_head()
    head = (xhead and xhead.s) or None
    if '???' == head:
        head = None
    return next((rule for rule in rules
                 if rule.x == type_ and rule.head == head), None)


def make_manner_rule(xmax: XMax) -> typing.Optional[Rule]:
    if not xmax.type == XType.N:
        return None
    xhead = xmax.to_head()
    manner = xhead and xhead.tags and xhead.tags['manner']
    if not manner:
        return None
    return Rule(
        x=xhead.type,
        head=xhead.s,
        vars=None,
        tree=['N-MAX', ['N-BAR', ['N', f'{xhead.s}_{manner}_N']]]
    )


def eval_var(rules: list[Rule],
             lcs: XMax,
             var_expansion: typing.Union[
                 str, typing.Callable[[TreeNode], TreeNode]]
             ) -> typing.Optional[TreeNode]:
    def mk_todo_subst(func_name):
        def todo_subst(_):
            return [f'TODO({func_name})']
        return todo_subst
    func = var_expansion
    if isinstance(func, str):
        if func == '#complement' or func == 'compl':
            func = to_complement
        elif func == 'spec':
            func = to_spec
        elif func == 'x2':
            func = to_x2
        elif func == 'x3':
            func = to_x3
        elif func == 'copy-spec':
            func = copy_spec
        elif func == 'copy-x2':
            func = copy_x2
        elif func == 'manner-x3':
            func = manner_x3
        else:
            func = mk_todo_subst(func)
    val = func(lcs)
    if (isinstance(val, list) or isinstance(val, tuple)) and len(val):
        if val[0] == 'none':
            val = None
        elif val[0] == 'node':
            val = val[1]
        elif val[0] == 'map':
            val = lcs_to_dtree(rules, val[1])
        elif val[0] == 'mapls':
            val = list(map(
                lambda node: lcs_to_dtree(rules, node),
                val[1]
            ))
        elif val[0] == 'subst':
            from_node = val[1]
            val = subst_vars(rules, lcs, from_node, None)
    return val


def subst_vars(rules: list[Rule],
               lcs: XMax,
               tree: TreeNode,
               variables: dict[str, TreeNode]) -> TreeNode:
    def level_to_iter(level: list[TreeNode]) -> typing.Iterable[TreeNode]:
        level = iter(level)
        try:
            while True:
                el = next(level)
                if el == '#,':
                    var_name = next(level)
                    val = eval_var(rules, lcs,
                                   variables.get(var_name, var_name
                                                 ) if variables else var_name)
                    if val is not None:
                        yield val
                elif el == '#,@':
                    var_name = next(level)
                    val = eval_var(rules,
                                   lcs,
                                   variables.get(var_name, var_name
                                                 ) if variables else var_name)
                    if val is not None:
                        yield from val
                elif el == '#,lcs':
                    rest = list(level)
                    lexp = subst_vars(rules, lcs, rest, variables)
                    mapped_lcs = lexp_to_tree(lexp)
                    if not isinstance(mapped_lcs, XMax):
                        print('subst_vars, macro >#,lcs<:',
                              'the mapped type should be XMax, got:',
                              type(mapped_lcs))
                    else:
                        mapped_tree = lcs_to_dtree(rules, mapped_lcs)
                        level = iter(mapped_tree)
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
        rule = make_manner_rule(lcs)
    if rule is None:
        return [f'TODO(no_rule_{lcs})']
    return subst_vars(rules, lcs, rule.tree, rule.vars)
