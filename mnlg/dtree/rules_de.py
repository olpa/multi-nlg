from mnlg.xbar import XType
from . import Rule
from .rules_en import RULES as RULES_EN


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


RULES = [
    gutnerkla_V,
    *RULES_EN,
]
