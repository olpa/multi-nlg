import typing

from mnlg.xbar import XMax, XSpecTag
from mnlg.transform import TreeNode


def dict_to_list(d: dict) -> list:
    keys = sorted(d.keys())
    return [[k, d[k]] for k in keys]


def to_tense_tags(xmax: XMax) -> list[str, str]:
    lcs_tags = xmax.to_head().tags
    tense = 'TPast' if 'pu' in lcs_tags else 'TPres'
    return dict_to_list({
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
            ) -> typing.Tuple[str, typing.Union[XMax, None, TreeNode]]:
    spec = xmax.to_spec()
    if isinstance(spec, XSpecTag):
        if 'le' in spec.tags:
            return 'node', ['tags', dict_to_list({'Det': 'DetSg'})]
        return 'none', None
    if not isinstance(spec, XMax):
        return 'none', None
    return 'map', spec


def to_x1(xmax: XMax) -> typing.Tuple[str, typing.Optional[XMax]]:
    func, compl = to_complement(xmax)
    if func == 'mapls' and compl:
        return 'map', compl[0]
