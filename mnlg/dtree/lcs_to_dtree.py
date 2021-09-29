import typing

from .functions import to_complement, to_spec, to_x2, to_x3
from .functions import copy_spec, copy_x2, manner_x3, tag_clitic_indirect
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
    manner = xhead and xhead.tags and xhead.tags.get('manner')
    if not manner:
        return None
    return Rule(
        x=xhead.type,
        head=xhead.s,
        vars=None,
        tree=['N-MAX', ['N-BAR', ['N', f'{xhead.s}_{manner}_N']]],
        adj=[],
    )


def eval_var(rules: list[Rule],
             lcs: XMax,
             var_expansion: typing.Union[
                 str, typing.Callable[[TreeNode], TreeNode]]
             ) -> typing.Optional[TreeNode]:
    def mk_todo_subst(func_name):
        def todo_subst(*_):
            return [f'TODO({func_name})']
        return todo_subst
    func = var_expansion
    args = None
    if isinstance(func, list):
        func, *args = func
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
        elif func == 'tag-clitic-indirect':
            func = tag_clitic_indirect
        else:
            func = mk_todo_subst(func)
    if args:
        val = func(lcs, *args)
    else:
        val = func(lcs)
    if (isinstance(val, list) or isinstance(val, tuple)) and len(val):
        if val[0] == 'none':
            val = None
        elif val[0] == 'node':
            val = val[1]
        elif val[0] == 'map':
            map_lcs = lexp_to_tree(val[1])
            val = lcs_to_dtree(rules, map_lcs)
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
                if el == '#,' or el == '#,@':
                    var_name = next(level)
                    var_expansion = variables.get(var_name, var_name
                                                  ) if variables else var_name
                    if isinstance(var_expansion, list):
                        var_expansion = subst_vars(
                            rules, lcs, var_expansion, variables)
                if el == '#,':
                    val = eval_var(rules, lcs, var_expansion)
                    if val is not None:
                        yield val
                elif el == '#,@':
                    val = eval_var(rules, lcs, var_expansion)
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


def adjunct(rules: list[Rule],
            lcs: XMax,
            rule: Rule,
            lexp_xmax: TreeNode
            ) -> TreeNode:
    if not rule.adj:
        return lexp_xmax
    if len(lexp_xmax) == 2:
        _, lexp_bar = lexp_xmax
        lexp_spec = None
    elif len(lexp_xmax) == 3:
        _, lexp_spec, lexp_bar = lexp_xmax
    else:
        print('lcs_to_dtree.adjunct: the xmax lexp should be',
              'of length 2 or 3, got:', len(lexp_xmax), lexp_xmax)
        return lexp_xmax

    def assert_name(node: TreeNode, name: str) -> bool:
        if not isinstance(node, list):
            print(f'lcs_to_dtree.adjunct: `{name}` check: node is not a list')
            return False
        if not len(node):
            print(f'lcs_to_dtree.adjunct: `{name}` check: node list is empty')
            return False
        node_name = node[0]
        if not isinstance(node_name, str):
            print(f'lcs_to_dtree.adjunct: `{name}` check:',
                  'node first element is not a string')
            return False
        if not node_name.endswith(name):
            if name == '-BAR' and not node_name.endswith('-FRAME'):
                print(f'lcs_to_dtree.adjunct: `{name}` check:',
                      f'does not match the node name `{node_name}`')
                return False
        return True

    if not assert_name(lexp_xmax, '-MAX'):
        return lexp_xmax
    if not assert_name(lexp_bar, '-BAR'):
        return lexp_xmax
    if lexp_spec and not assert_name(lexp_spec, '-SPEC'):
        return lexp_xmax

    bar_name = f'{lexp_xmax[0][0]}-BAR'
    for adj in rule.adj:
        expanded_adj = subst_vars(rules, lcs, adj, rule.vars)
        if not assert_name(expanded_adj, '-MAX'):
            print(f'lcs_to_dtree.adjunct: adj before: `{adj}`,',
                  f'adj after rewrite: `{expanded_adj}`')
            continue
        lexp_bar = [bar_name, lexp_bar, expanded_adj]

    if lexp_spec:
        return [lexp_xmax[0], lexp_spec, lexp_bar]
    return [lexp_xmax[0], lexp_bar]


def lcs_to_dtree(rules: list[Rule], lcs: XMax) -> TreeNode:
    rule = find_rule(rules, lcs)
    if rule is None:
        rule = make_manner_rule(lcs)
    if rule is None:
        return [f'TODO(no_rule_{lcs})']
    base = subst_vars(rules, lcs, rule.tree, rule.vars)
    return adjunct(rules, lcs, rule, base)
