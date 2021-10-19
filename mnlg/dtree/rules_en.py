from mnlg.xbar import XType
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

midju_V = Rule(
    x=XType.V,
    head='midju',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'be_V'],
           ['N-MAX',
            ['#,', 'adjunct',
             ['#,', 'adjunct',
              ['N-BAR', ['N', 'midju_N']],
              ['#,', 'lcs-adj-bar']],
             ['P-MAX',
              ['P-BAR',
               ['P', 'of_Prep'],
               ['#,', 'x2']]]]]]],
    vars=None,
    adj=[]
)

san_francisco_PN = Rule(
    x=XType.N,
    head='sanfransiskos',
    tree=['N-MAX', ['N-BAR', ['N', 'san_francisco_PN']]],
    vars=None,
    adj=[],
)

north_california_PN = Rule(
    x=XType.N,
    head='nosenkalifornos',
    tree=['N-MAX', ['N-BAR', ['N', 'north_california_PN']]],
    vars=None,
    adj=[],
)

kulnu_A = Rule(
    x=XType.A,
    head='kulnu',
    tree=['A-MAX', ['A-BAR', ['A', 'kulnu_A']]],
    vars=None,
    adj=[],
)

canja_A = Rule(
    x=XType.A,
    head='canja',
    tree=['A-MAX', ['A-BAR', ['A', 'canja_A']]],
    vars=None,
    adj=[],
)

jdini_A = Rule(
    x=XType.A,
    head='jdini',
    tree=['A-MAX', ['A-BAR', ['A', 'jdini_A']]],
    vars=None,
    adj=[],
)

RULES = [
    *RULES_RGL,
    darxi_V,
    djan_N,
    gutnerkla_V,
    midju_V,
    kumfa_N,
    san_francisco_PN,
    north_california_PN,
    kulnu_A,
    canja_A,
    jdini_A,
]
