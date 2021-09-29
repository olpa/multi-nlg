from mnlg.xbar import XType, XMax
from . import Rule
from .functions import dict_to_tags
from .rules_rgl import RULES_RGL


def to_tense_tags_es(xmax: XMax) -> list[list[str, str]]:
    tags = xmax.to_head().tags or {}
    tense = 'TPasseSimple' if tags and 'pu' in tags else 'TPres'
    return dict_to_tags({
        'Tense': tense,
        'Ant': 'ASimul',
    })


tense_rule = Rule(
    x=XType.I,
    head=None,
    tree=['I-MAX', ['I-BAR',
                    ['I', '#,@', 'tags'], '#,@', 'compl']],
    vars={
        'tags': to_tense_tags_es,
    },
    adj=[],
)

gutnerkla_V = Rule(
    x=XType.V,
    head='gutnerkla',
    tree=['#,lcs',
          'V-MAX',
          '#,', 'copy-spec',
          ['V-FRAME',
           ['V', 'bapli'],
           ['D-MAX',
            ['D-BAR',
             ['D', ["tag", "le"]],
             ['N-MAX',
              ['N-BAR',
               ['N', 'nerkla'],
               '#,', 'copy-x2']]]]]],
    vars=None,
    adj=[],
)

bapli_V = Rule(
    x=XType.V,
    head='bapli',
    vars=None,
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR', ['V', 'force_V'], '#,', 'x2']],
    adj=[],
)

nerkla_N = Rule(
    x=XType.N,
    head='nerkla',
    vars=None,
    tree=['N-MAX',
          ['N-BAR', ['N', 'entrance_N']]],
    adj=[
        ['P-MAX',
         ['P-BAR',
          ['P', 'to_Prep'],
          '#,', 'x2']]
    ],
)

kumfa_N = Rule(
    x=XType.N,
    head='kumfa',
    vars=None,
    tree=['N-MAX',
          ['N-BAR', ['N', 'room_N']]],
    adj=[],
)

djan_N = Rule(
    x=XType.N,
    head='djan',
    tree=['N-MAX', ['N-BAR', ['N', 'john_PN']]],
    vars=None,
    adj=[],
)

darxi_V = Rule(
    x=XType.V,
    head='darxi',
    vars=None,
    tree=['#,lcs',
          'V-MAX',
          '#,', 'copy-spec',
          ['V-FRAME',
           ['V', 'dunda'],
           '#,', 'copy-x2',
           '#,', 'manner-x3',
           ]],
    adj=[],
)

dunda_V = Rule(
    x=XType.V,
    head='dunda',
    vars=None,
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR',
           ['V', 'give_V3'],
           ['V-MAX',
            ['V-SPEC', '#,', 'x2'],
            ['V-BAR',
             ['V', ['tag', 'trace']],
             '#,', 'x3'
             ]]]],
    adj=[
        ['#,@', ['tag-clitic-indirect', ['#,@', 'x2']]],
    ],
)

RULES = [
    tense_rule,
    *RULES_RGL,
    gutnerkla_V,
    bapli_V,
    darxi_V,
    dunda_V,
    nerkla_N,
    kumfa_N,
    djan_N,
]
