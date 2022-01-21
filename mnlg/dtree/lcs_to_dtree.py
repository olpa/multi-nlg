from __future__ import annotations
import sys
import typing
from collections import abc

from .functions import to_complement, to_spec, to_x1, to_x2, to_x3
from .functions import copy_spec, copy_x1, copy_x2, manner_x3, copy_self
from .functions import tag_clitic_indirect, attach_adjunct, lcs_adj_bar
from .functions import to_tags
from .types import Rule, LcsToDtreeContext
from lxslt import TreeNode
from lojban_xbar import lexp_to_tree, XMax, XType
from lojban_xbar import is_max_node, is_bar_node, is_spec_node


def find_rule(
        rules: list[Rule],
        xmax: XMax,
        xtype: typing.Optional[XType] = None
) -> typing.Optional[Rule]:
    if xtype is None or xmax.type == XType.J:
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
        elif func == 'self':
            func = copy_self
        elif func == 'tags':
            func = to_tags
        else:
            func = None
    if not func:
        print('eval_var: no such function:', func_name, file=sys.stderr)
        return ['#', *var_expansion]

    if func_name.startswith('lcs-'):
        if not args:
            args = []
        args.append(LcsToDtreeContext(rules, lcs_to_dtree))
    if args:
        val = func(lcs, *args)
    else:
        val = func(lcs)
    if (isinstance(val, list) or isinstance(val, tuple)) and len(val):
        xtype = next(
            filter(lambda sy: isinstance(sy, str) and len(sy) == 1,
                   iter(val)),
            None)
        if xtype:
            try:
                xtype = XType[xtype]
            except KeyError:
                print('eval_var: unsupported scan type:',
                      xtype, file=sys.stderr)
                xtype = None
        if lcs.type == XType.J and not xtype:
            xtype = XType.A

        if val[0] == 'none':
            val = None
        elif val[0] == 'node':
            val = val[1]
        elif val[0] == 'map':
            map_lcs = lexp_to_tree(val[1])
            val = lcs_to_dtree(rules, map_lcs, xtype)
        elif val[0] == 'mapls':
            val = list(map(
                lambda node: lcs_to_dtree(rules, node, xtype),
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

        return 'rescan_tree', node

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
            if len(arg) == 1:
                rescan_tree, rescan_type = arg[0], None
            elif len(arg) == 2:
                rescan_tree, rescan_type = arg
                try:
                    rescan_type = XType[rescan_type]
                except KeyError:
                    print('cmd_exec_iter: unknown XType in rescan:',
                          rescan_type, file=sys.stderr)
                    rescan_type = None
            else:
                print('cmd_exec_iter: only one argument expected, got:',
                      arg, file=sys.stderr)
                yield [cmd, arg]
                return
            lexp = subst_vars(rules, lcs, rescan_tree, variables)
            mapped_lcs = lexp_to_tree(lexp)
            if not isinstance(mapped_lcs, XMax):
                print('subst_vars, macro >#,lcs<:',
                      'the mapped type should be XMax, got:',
                      type(mapped_lcs))
            else:
                mapped_tree = lcs_to_dtree(rules, mapped_lcs, rescan_type)
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
            elif cmd == 'rescan_tree':
                yield list(subst_rec_iter(arg))
            else:
                assert False, f'never reached: unknown command `{cmd}`'

    processed = list(subst_rec_iter([tree]))
    if not processed:
        return None
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
              'of length 2 or 3, got:', len(lexp_xmax), lexp_xmax,
              file=sys.stderr)
        return lexp_xmax

    if not is_max_node(lexp_xmax):
        print('lcs_to_dtree.adjunct: X-MAX is expected, got:', lexp_xmax,
              file=sys.stderr)
        return lexp_xmax
    if not is_bar_node(lexp_bar):
        print('lcs_to_dtree.adjunct: X-BAR is expected, got:', lexp_bar,
              file=sys.stderr)
        return lexp_xmax
    if lexp_spec and not is_spec_node(lexp_spec):
        print('lcs_to_dtree.adjunct: X-SPEC is expected, got:', lexp_spec,
              file=sys.stderr)
        return lexp_xmax

    bar_name = f'{lexp_xmax[0][0]}-BAR'
    for adj in rule.adj:
        expanded_adj = subst_vars(rules, lcs, adj, rule.vars)
        if expanded_adj is None:
            continue

        if is_max_node(expanded_adj):
            lexp_bar = [bar_name, lexp_bar, expanded_adj]
            continue

        if not is_bar_node(expanded_adj):
            print('lcs_to_dtree.adjunct: X-MAX or X-BAR is expected after'
                  f'rewrite, adj before: `{adj}`, adj after rewrite:'
                  f'`{expanded_adj}`', file=sys.stderr)
            continue

        lexp_bar = attach_adjunct(lcs, lexp_bar, expanded_adj)

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
        print_type = f'{xtype}_'if xtype and xtype != lcs.type else ''
        return [f'TODO(no_rule_{print_type}{lcs})']
    base = subst_vars(rules, lcs, rule.tree, rule.vars)
    augmented = adjunct(rules, lcs, rule, base)
    return augmented
