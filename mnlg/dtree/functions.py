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


def to_det_tags(xmax: XMax) -> list[list[str, str]]:
    tags = xmax.to_head().tags or {}
    if 'loi' in tags:
        return dict_to_tags({'mass': 'mass'})
    quant = 'DefArt' if 'le' in tags else 'IndefArt'
    num = 'NumSg'
    return dict_to_tags({
        'Quant': quant,
        'Num': num,
    })


def to_complement(xmax: XMax) -> typing.Tuple[str, list[XMax]]:
    compl = xmax.to_complement()
    if not compl:
        return 'mapls', []
    if not isinstance(compl, list) and not isinstance(compl, tuple):
        compl = [compl]
    return 'mapls', compl or []


def to_spec(xmax: XMax
            ) -> typing.Tuple[str, typing.Union[XMax, None, TreeNode]]:
    spec = xmax.to_spec()
    if isinstance(spec, XSpecTag):
        if spec.tags and 'le' in spec.tags:
            return 'node', dict_to_tags({'Det': 'DetSg'})
        return 'none', None
    if not isinstance(spec, XMax):
        return 'none', None
    return 'map', spec


def to_x2(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and compl:
        return 'map', compl[0]


def to_x3(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and len(compl) >= 2:
        return 'map', compl[1]


def copy_spec(xmax: XMax) -> typing.Optional[XSpec]:
    return xmax.to_spec().to_lexp()


def copy_x2(xmax: XMax) -> typing.Optional[XSpec]:
    bar = xmax.to_bar()
    if isinstance(bar, XBarBase):
        return bar.compl.to_lexp()
    if isinstance(bar, XBarFrame):
        compl = bar.compl
        if isinstance(compl, tuple) and compl:
            return compl[0].to_lexp()
    return None


def manner_x3(xmax: XMax) -> typing.Optional[TreeNode]:
    x_ext_head = xmax.to_head()
    s_ext = x_ext_head and x_ext_head.s
    if not s_ext:
        print('manner_meaning: required: external head. got xmax:',
              xmax, file=sys.stderr)
        return None

    compl = xmax.to_complement()
    if len(compl) < 2:
        print('manner_meaning_x3: required: x3 for xmax:',
              xmax, file=sys.stderr)
        return None

    x_int_max = compl[1]
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
    dtree_d = ['D-MAX', ['D-BAR', ['D', ['tag', 'loi']], dtree_n]]

    return dtree_d
