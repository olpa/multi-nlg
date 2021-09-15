from .functions import to_tense_tags
from .types import Rule
from mnlg.xbar import XType


tense_rule = Rule(
    x=XType.I,
    head=None,
    tree=['I-MAX', ['I-BAR', ['I', None,
                              ['tags', '#,', 'tags']], '#,@', 'compl']],
    vars={
        'tags': to_tense_tags,
        'compl': '#complement',
    }
)

mi_Pron = Rule(
    x=XType.N,
    head='mi',
    tree=['N-MAX', ['N-BAR', ['N', 'i_Pron']]],
    vars=None,
)
