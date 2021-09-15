from mnlg.xbar import XType
from . import Rule
from .rules_rgl import tense_rule, mi_Pron

darxi_V = Rule(
    x=XType.V,
    head='darxi',
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR', ['V', 'stab_V'], '#,', 'x1']],
    vars=None
)

djan_N = Rule(
    x=XType.N,
    head='djan',
    tree=['N-MAX', ['N-BAR', ['N', 'john_N']]],
    vars=None,
)

RULES = [
    darxi_V,
    tense_rule,
    mi_Pron,
    djan_N,
]
