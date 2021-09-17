from mnlg.xbar import XType
from . import Rule
from .rules_rgl import tense_rule, mi_Pron

darxi_V = Rule(
    x=XType.V,
    head='darxi',
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR', ['V', 'stab_V2'], '#,', 'x1']],
    vars=None
)

djan_N = Rule(
    x=XType.N,
    head='djan',
    tree=['N-MAX', ['N-BAR', ['N', 'john_PN']]],
    vars=None,
)

kumfa_N = Rule(
    x=XType.N,
    head='kumfa',
    tree=['N-MAX', ['N-SPEC', '#,', 'spec'], ['N-BAR', ['N', 'room_N']]],
    vars=None,
)

gutnerkla_V = Rule(
    x=XType.V,
    head='gutnerkla',
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR', ['V', 'break_V'],
           ['P-MAX', ['P-BAR', ['P', 'into_P'], '#,', 'x1']]]],
    vars=None
)

RULES = [
    darxi_V,
    tense_rule,
    mi_Pron,
    djan_N,
    gutnerkla_V,
    kumfa_N,
]
