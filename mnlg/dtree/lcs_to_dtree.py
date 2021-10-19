import sys
import typing
from collections import abc

from .functions import to_complement, to_spec, to_x1, to_x2, to_x3
from .functions import copy_spec, copy_x1, copy_x2, manner_x3
from .functions import tag_clitic_indirect, attach_adjunct, lcs_adj_bar
from .types import Rule, LcsToDtreeContext
from ..transform import TreeNode
from mnlg.xbar import lexp_to_tree, XMax, XType


def find_rule(
        rules: list[Rule],
        xmax: XMax,
        xtype: typing.Optional[XType] = None
) -> typing.Optional[Rule]:
    if xtype is None:
        xtype = xmax.type
    xhead = xmax.to_head()
    head = (xhead and xhead.s) or None
    if '???' == head:
        head = None
    return next((rule for rule in rules
                 if rule.x == xtype and rule.head == head), None)


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
        tree=['N-MAX', ['N-BAR', ['N', f'{xhead.s}_{manner}_CN']]],
        adj=[],
    )


def eval_var(rules: list[Rule],
             lcs: XMax,
             var_expansion: typing.Union[
                 str, typing.Callable[[TreeNode], TreeNode]]
             ) -> typing.Optional[TreeNode]:
    def mk_todo_subst(subst_func_name):
        def todo_subst(*_):
            return [f'TODO({subst_func_name})']
        return todo_subst
    func = var_expansion
    args = None
    if isinstance(func, list):
        func, *args = func
    func_name = func if isinstance(func, str) else ''
    if func_name:
        if func == '#complement' or func == 'compl':
            func = to_complement
        elif func == 'spec':
            func = to_spec
        elif func == 'x1':
            func = to_x1
        elif func == 'x2':
            func = to_x2
        elif func == 'x3':
            func = to_x3
        elif func == 'copy-spec':
            func = copy_spec
        elif func == 'copy-x1':
            func = copy_x1
        elif func == 'copy-x2':
            func = copy_x2
        elif func == 'manner-x3':
            func = manner_x3
        elif func == 'tag-clitic-indirect':
            func = tag_clitic_indirect
        elif func == 'lcs-adj-bar':
            func = lcs_adj_bar
        elif func == 'adjunct':
            func = attach_adjunct
        else:
            func = mk_todo_subst(func)
    if func_name.startswith('lcs-'):
        if not args:
            args = []
        args.append(LcsToDtreeContext(rules, lcs_to_dtree))
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

    def to_cmd(
            node: TreeNode
    ) -> typing.Tuple[str, typing.Union[TreeNode, list[TreeNode]]]:
        if isinstance(node, str):
            return 'leaf', node
        if not isinstance(node, abc.Sequence):
            return 'leaf', node
        if not node:
            return 'leaf', []
        cmd = node[0]

        ls_cmd_one_arg = ('#,', '#,@', '#,lcs')
        if cmd in ls_cmd_one_arg:
            if len(node) < 2:
                print('subst_vars: expected at least one argument to',
                      f'''>{'<,>'.join(ls_cmd_one_arg)}<, got:''', node,
                      file=sys.stderr)
                return 'leaf', node
            return cmd, node[1:]

        return 'tree', node

    def cmd_exec_iter(
            cmd: str, arg: list[TreeNode]
    ) -> typing.Iterable[TreeNode]:
        if cmd == '#,' or cmd == '#,@':
            var_name = arg[0]
            if variables and var_name in variables:
                var_expansion = variables[var_name]
                if len(arg) > 1:
                    print('cmd_exec_iter: present both but should be',
                          'exclusive: variable expansion and function',
                          'arguments: expansion:', var_expansion,
                          ', command:', arg, file=sys.stderr)
            else:
                var_expansion = arg

            if isinstance(var_expansion, list):
                var_expansion = subst_vars(
                    rules, lcs, var_expansion, variables)

            if cmd == '#,':
                val = eval_var(rules, lcs, var_expansion)
                if val is not None:
                    yield val
                return

            if cmd == '#,@':
                val = eval_var(rules, lcs, var_expansion)
                if val is not None:
                    yield from val
                return

            assert False, 'never reached: unknown command'

        if cmd == '#,lcs':
            if len(arg) != 1:
                print('cmd_exec_iter: only one argument expected, got:',
                      arg, file=sys.stderr)
            if not arg:
                yield [cmd, arg]
                return
            lexp = subst_vars(rules, lcs, arg[0], variables)
            mapped_lcs = lexp_to_tree(lexp)
            if not isinstance(mapped_lcs, XMax):
                print('subst_vars, macro >#,lcs<:',
                      'the mapped type should be XMax, got:',
                      type(mapped_lcs))
            else:
                mapped_tree = lcs_to_dtree(rules, mapped_lcs)
                yield mapped_tree
            return

        assert False, 'never reached: unknown command'

    def subst_rec_iter(node: TreeNode) -> typing.Iterable[TreeNode]:
        for kid in node:
            cmd, arg = to_cmd(kid)
            if cmd == 'leaf':
                yield kid
            elif cmd.startswith('#'):
                yield from cmd_exec_iter(cmd, arg)
            elif cmd == 'tree':
                yield list(subst_rec_iter(arg))
            else:
                assert False, f'never reached: unknown command `{cmd}`'

    processed = list(subst_rec_iter([tree]))
    if len(processed) != 1:
        print('subst_vars: resulting node-set should be of length 1,',
              f'got length {len(processed)}')
    return processed[0] if processed else tree


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


def lcs_to_dtree(
        rules: list[Rule],
        lcs: XMax,
        xtype: typing.Optional[XType] = None
) -> TreeNode:
    rule = find_rule(rules, lcs, xtype)
    if rule is None:
        rule = make_manner_rule(lcs)
    if rule is None:
        return [f'TODO(no_rule_{lcs})']
    base = subst_vars(rules, lcs, rule.tree, rule.vars)
    return adjunct(rules, lcs, rule, base)
