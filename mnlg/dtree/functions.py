import sys
import typing

from mnlg.xbar import XMax, XSpecTag, XSpec, XBarBase, XBarFrame, XType
from mnlg.transform import TreeNode


def dict_to_tags(d: dict) -> list[list[str]]:
    keys = sorted(d.keys())
    return [['tag', k] if k == d[k] else ['tag', k, d[k]] for k in keys]


def to_tense_tags(xmax: XMax) -> list[list[str, str]]:
    tags = xmax.to_head().tags or {}
    tense = 'TPast' if tags and 'pu' in tags else 'TPres'
    return dict_to_tags({
        'Tense': tense,
        'Ant': 'ASimul',
    })


def to_complement(xmax: XMax) -> typing.Tuple[str, list[XMax]]:
    compl = xmax.to_complement()
    if not compl:
        return 'mapls', []
    if not isinstance(compl, list) and not isinstance(compl, tuple):
        compl = [compl]
    return 'mapls', compl or []


def to_spec(xmax: XMax
            ) -> typing.Tuple[str, typing.Union[None, TreeNode]]:
    spec = xmax.to_spec()
    if isinstance(spec, XSpecTag):
        return 'node', spec.to_lexp()[1:]  # Drop 'X-SPEC' prefix
    if isinstance(spec, XMax):
        return 'map', spec.to_lexp()
    return 'none', None


def to_x1(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and compl:
        return 'map', compl[0]


def to_x2(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and len(compl) >= 2:
        return 'map', compl[1]


def to_x3(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and len(compl) >= 3:
        return 'map', compl[2]


def copy_spec(xmax: XMax) -> typing.Optional[XSpec]:
    xspec = xmax.to_spec()
    return xspec.to_lexp() if xspec else None


def copy_xn(xmax: XMax, n: int) -> typing.Optional[XSpec]:
    bar = xmax.to_bar()
    if isinstance(bar, XBarBase):
        return bar.compl.to_lexp()
    if isinstance(bar, XBarFrame):
        compl = bar.compl
        if isinstance(compl, tuple) and compl:
            if len(compl) > n - 1:
                return compl[n - 1].to_lexp()
    return None


def copy_x1(xmax: XMax) -> typing.Optional[XSpec]:
    return copy_xn(xmax, 1)


def copy_x2(xmax: XMax) -> typing.Optional[XSpec]:
    return copy_xn(xmax, 2)


def manner_x3(xmax: XMax) -> typing.Optional[TreeNode]:
    x_ext_head = xmax.to_head()
    s_ext = x_ext_head and x_ext_head.s
    if not s_ext:
        print('manner_meaning: required: external head. got xmax:',
              xmax, file=sys.stderr)
        return None

    compl = xmax.to_complement()
    if len(compl) < 3:
        print('manner_meaning_x3: required: x3 for xmax:',
              xmax, file=sys.stderr)
        return None

    x_int_max = compl[2]
    if x_int_max.type == XType.D:
        x_int_max = x_int_max.to_complement()
        if not x_int_max:
            print('manner_meaning_x3: required: x3 for xmax,',
                  'but determiner does not have a complement:',
                  xmax, file=sys.stderr)
            return None

    x_int_head = x_int_max.to_head()
    s_int = x_int_head and x_int_head.s
    if not s_int:
        print('manner_meaning: required: internal head. got internal xmax:',
              x_int_max, file=sys.stderr)
        return None

    dtree_n = ['N-MAX', ['N-BAR', ['N', ['tag', 'manner', s_int], s_ext]]]
    dtree_d = ['D-MAX', ['D-BAR', ['D', 'loi'], dtree_n]]

    return dtree_d


def tag_xmax(lexp_xmax: TreeNode,
             tag_expr: list[str],  # ['tag', 'tag-name', 'tag-value']
             ) -> typing.Optional[TreeNode]:
    nmax_seen = False
    tag_added = False

    def augment_tree_rec(tree: TreeNode) -> TreeNode:
        nonlocal nmax_seen
        if not isinstance(tree, list):
            return tree
        if not len(tree):
            return []
        ename = tree[0]
        if (ename.endswith('-BAR')
                or ename.endswith('-FRAME')
                or (ename.endswith('-MAX') and (not nmax_seen))):
            nmax_seen = True
            return list(map(augment_tree_rec, tree))

        def maybe_expand():
            nonlocal tag_added
            level = iter(tree)
            yield next(level)
            if len(ename) == 1:
                tag_added = True
                yield tag_expr
            yield from level
        return list(maybe_expand())

    back = augment_tree_rec(lexp_xmax)
    if not tag_added:
        print('tag_xmax: could not find a place for tags in the tree',
              lexp_xmax, file=sys.stderr)
    return back


def tag_clitic_indirect(_: XMax,
                        lexp_xmax: TreeNode
                        ) -> typing.Optional[TreeNode]:
    return tag_xmax(lexp_xmax, ['tag', 'clitic', 'indirect'])
