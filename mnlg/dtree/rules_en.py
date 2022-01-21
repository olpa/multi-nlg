from lojban_xbar import XType
from . import Rule
from .rules_rgl import RULES_RGL

darxi_V = Rule(
    x=XType.V,
    head='darxi',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'stab_V2'], ['#,', 'x2']]],
    vars=None,
    adj=[],
)

djan_N = Rule(
    x=XType.N,
    head='djan',
    tree=['N-MAX', ['N-BAR', ['N', 'john_PN']]],
    vars=None,
    adj=[],
)

kumfa_N = Rule(
    x=XType.N,
    head='kumfa',
    tree=['N-MAX', ['N-SPEC', ['#,', 'x1']], ['N-BAR', ['N', 'room_N']]],
    vars=None,
    adj=[],
)

gutnerkla_V = Rule(
    x=XType.V,
    head='gutnerkla',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'break_into_V'],
           ['#,', 'x2']]],
    vars=None,
    adj=[],
)

RULES = [
    darxi_V,
    djan_N,
    gutnerkla_V,
    kumfa_N,
    *RULES_RGL,
]
