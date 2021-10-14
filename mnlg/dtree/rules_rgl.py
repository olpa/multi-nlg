from .functions import to_tense_tags
from .types import Rule
from mnlg.xbar import XType


tense_rule = Rule(
    x=XType.I,
    head=None,
    tree=['I-MAX', ['I-BAR',
                    ['I', '#,@', 'tags'], '#,@', 'compl']],
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
                    '#,@', 'compl']],
    vars=None,
    adj=[],
)

loi_Det = Rule(
    x=XType.D,
    head='loi',
    tree=['D-MAX', ['D-BAR',
                    ['D', ['tag', 'mass']],
                    '#,@', 'compl']],
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

RULES_RGL = [
    tense_rule,
    le_Det,
    loi_Det,
    mi_Pron,
]
