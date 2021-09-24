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
                    ['I', None, '#,@', 'tags'], '#,@', 'compl']],
    vars={
        'tags': to_tense_tags_es,
    }
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
    vars=None
)

bapli_V = Rule(
    x=XType.V,
    head='bapli',
    vars=None,
    tree=['V-MAX',
          ['V-SPEC', '#,', 'spec'],
          ['V-BAR', ['V', 'force_V2'], '#,', 'x2']]
)

nerkla_N = Rule(
    x=XType.N,
    head='nerkla',
    vars=None,
    tree=['N-MAX',
          ['N-BAR', ['N', 'entrance_N'],
           ['P-MAX',
            ['P-BAR',
             ['P', 'to_Prep'],
             '#,', 'x2']]]],
)

kumfa_N = Rule(
    x=XType.N,
    head='kumfa',
    vars=None,
    tree=['N-MAX',
          ['N-BAR', ['N', 'room_N']]]
)

djan_N = Rule(
    x=XType.N,
    head='djan',
    tree=['N-MAX', ['N-BAR', ['N', 'john_PN']]],
    vars=None,
)

RULES = [
    tense_rule,
    *RULES_RGL,
    gutnerkla_V,
    bapli_V,
    nerkla_N,
    kumfa_N,
    djan_N,
]