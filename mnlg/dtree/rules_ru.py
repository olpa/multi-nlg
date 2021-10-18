from .rules_rgl import RULES_RGL
from mnlg.xbar import XType
from . import Rule


darxi_V = Rule(
    x=XType.V,
    head='darxi',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'hit_V'], ['#,', 'x2'],
           ]],
    vars=None,
    adj=[
        ['P-MAX', ['P-BAR', ['P', 'ins_Prep'], ['#,', 'x3']]]
    ],
)

gutnerkla_V = Rule(
    x=XType.V,
    head='gutnerkla',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR',
           ['V-BAR', ['V', 'break_into_V']],
           ['P-MAX', ['P-BAR', ['P', 'into_Prep'], ['#,', 'x2']]]
           ]],
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

dakfu_N = Rule(
    x=XType.N,
    head='dakfu',
    tree=['N-MAX', ['N-SPEC', ['#,', 'x1']], ['N-BAR', ['N', 'knife_N']]],
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


RULES = [
    *RULES_RGL,
    darxi_V,
    gutnerkla_V,
    djan_N,
    dakfu_N,
    kumfa_N,
]
