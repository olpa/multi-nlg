from .functions import to_tense_tags, to_det_tags
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

det_rule = Rule(
    x=XType.D,
    head=None,
    tree=['D-MAX', ['D-BAR',
                    ['D', '#,@', 'tags'], '#,@', 'compl']],
    vars={
        'tags': to_det_tags,
    },
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
    det_rule,
    mi_Pron,
]
