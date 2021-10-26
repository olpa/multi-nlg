from .functions import to_tense_tags
from .types import Rule
from mnlg.xbar import XType


tense_rule = Rule(
    x=XType.I,
    head=None,
    tree=['I-MAX', ['I-BAR',
                    ['I', ['#,@', 'tags']], ['#,@', 'compl']]],
    vars={
        'tags': to_tense_tags,
    },
    adj=[],
)

le_Det = Rule(
    x=XType.D,
    head='le',
    tree=['D-MAX', ['D-BAR',
                    ['D',
                     ['tag', 'Num', 'NumSg'],
                     ['tag', 'Quant', 'DefArt']],
                    ['#,@', 'compl']]],
    vars=None,
    adj=[],
)

loi_Det = Rule(
    x=XType.D,
    head='loi',
    tree=['D-MAX', ['D-BAR',
                    ['D', ['tag', 'mass']],
                    ['#,@', 'compl']]],
    vars=None,
    adj=[],
)

mi_Pron = Rule(
    x=XType.N,
    head='mi',
    tree=['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'i_Pron']]],
    vars=None,
    adj=[],
)

empty_J = Rule(
    x=XType.J,
    head=None,
    tree=['J-MAX', ['J-BAR', ['J', ''], ['#,@', 'compl']]],
    vars=None,
    adj=[['#,', 'lcs-adj-bar']],
)

je_J = Rule(
    x=XType.J,
    head='je',
    tree=['J-MAX', ['J-BAR', ['J', 'je'], ['#,@', 'compl']]],
    vars=None,
    adj=[['#,', 'lcs-adj-bar']],
)

midju_V = Rule(
    x=XType.V,
    head='midju',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'be_V'],
           ['D-MAX',
            ['D-BAR',
             ['D', ['tag', 'Quant', 'DefArt'], 'le'],
             ['N-MAX',
              ['#,', 'adjunct',
               ['#,', 'adjunct',
                ['N-BAR', ['N', 'center_N']],
                ['#,', 'lcs-adj-bar']],
               ['P-MAX',
                ['P-BAR',
                 ['P', 'of_Prep'],
                 ['#,', 'x2']]]]]]]]],
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
    tree=['A-MAX', ['A-BAR', ['A', 'cultural_A']]],
    vars=None,
    adj=[],
)

canja_A = Rule(
    x=XType.A,
    head='canja',
    tree=['A-MAX', ['A-BAR', ['A', 'commercial_A']]],
    vars=None,
    adj=[],
)

jdini_A = Rule(
    x=XType.A,
    head='jdini',
    tree=['A-MAX', ['A-BAR', ['A', 'financial_A']]],
    vars=None,
    adj=[],
)

xunre_V = Rule(
    x=XType.V,
    head='xunre',
    vars=None,
    tree=['V-MAX', ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'be_V'],
           ['#,lcs', ['#,', 'self'], 'A']]],
    adj=[],
)

xunre_A = Rule(
    x=XType.A,
    head='xunre',
    vars=None,
    tree=['A-MAX', ['A-BAR', ['A', 'red_A']]],
    adj=[['#,', 'lcs-adj-bar']],
)

blanu_A = Rule(
    x=XType.A,
    head='blanu',
    vars=None,
    tree=['A-MAX', ['A-BAR', ['A', 'blue_A']]],
    adj=[['#,', 'lcs-adj-bar']],
)

RULES_RGL = [
    tense_rule,
    le_Det,
    loi_Det,
    mi_Pron,
    empty_J,
    je_J,
    midju_V,
    san_francisco_PN,
    north_california_PN,
    kulnu_A,
    canja_A,
    jdini_A,
    xunre_V,
    xunre_A,
    blanu_A,
]
