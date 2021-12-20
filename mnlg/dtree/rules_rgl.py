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

do_Pron = Rule(
    x=XType.N,
    head='do',
    tree=['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'youSg_Pron']]],
    vars=None,
    adj=[],
)

je_J = Rule(
    x=XType.J,
    head='je',
    tree=['J-MAX', ['J-BAR', ['J', ['#,@', 'tags'], 'je'],
                    ['#,@', 'compl']]],
    vars=None,
    adj=[['#,', 'lcs-adj-bar']],
)

ceho_J = Rule(
    x=XType.J,
    head="ce'o",
    tree=['J-MAX', ['J-BAR', ['J', ['#,@', 'tags'], "ce'o"],
                    ['#,@', 'compl', 'N']]],
    vars=None,
    adj=[['#,', 'lcs-adj-bar', 'N']],
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

koha_N = Rule(
    x=XType.N,
    head="ko'a",
    tree=['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'it_Pron']]],
    vars=None,
    adj=[],
)

san_francisco_PN = Rule(
    x=XType.N,
    head='sanfransiskos',
    tree=['N-MAX', ['N-BAR', ['N', 'san_francisco_PN']]],
    vars=None,
    adj=[],
)

los_angeles_PN = Rule(
    x=XType.N,
    head='losangeles',
    tree=['N-MAX', ['N-BAR', ['N', 'los_angeles_PN']]],
    vars=None,
    adj=[],
)

san_diego_PN = Rule(
    x=XType.N,
    head="sandi'egos",
    tree=['N-MAX', ['N-BAR', ['N', 'san_diego_PN']]],
    vars=None,
    adj=[],
)

san_jose_PN = Rule(
    x=XType.N,
    head='sanjoses',
    tree=['N-MAX', ['N-BAR', ['N', 'san_jose_PN']]],
    vars=None,
    adj=[],
)

california_PN = Rule(
    x=XType.N,
    head='kalifornos',
    tree=['N-MAX', ['N-BAR', ['N', 'california_PN']]],
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

moi_A = Rule(
    x=XType.A,
    head='moi',
    vars=None,
    tree=['#,lcs', ['#,', 'copy-spec'], 'A'],
    adj=[
        ['P-MAX', ['P-BAR',
                   ['P', ['tag', 'elide_article'], 'by_Prep'],
                   ['#,', 'x3']]],
        ['#,', 'lcs-adj-bar']],
)

vo_A = Rule(
    x=XType.A,
    head='vo',
    vars=None,
    tree=['A-MAX', ['A-BAR', ['A', 'fourth_A']]],
    adj=[],
)

lidne_A = Rule(
    x=XType.A,
    head='lidne',
    vars=None,
    tree=['P-MAX', ['P-BAR',
                    ['P', 'after_Prep'],
                    ['#,', 'x1']]],
    adj=[],
)

xahugri_N = Rule(
    x=XType.N,
    head="xa'ugri",
    tree=['N-MAX', ['N-SPEC', ['#,', 'x1']], ['N-BAR', ['N', 'population_N']]],
    vars=None,
    adj=[],
)

tcadu_V = Rule(
    x=XType.V,
    head='tcadu',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'be_V'],
           ['D-MAX',
            ['D-BAR',
             ['D', ['tag', 'Quant', 'DefArt'], 'le'],
             ['N-MAX',
              ['#,', 'adjunct',
               ['#,', 'adjunct',
                ['N-BAR', ['N', 'city_N']],
                ['#,', 'lcs-adj-bar']],
               ['P-MAX',
                ['P-BAR',
                 ['P', 'of_Prep'],
                 ['#,', 'x2']]]]]]]]],
    vars=None,
    adj=[]
)

prami_V = Rule(
    x=XType.V,
    head='prami',
    tree=['V-MAX',
          ['V-SPEC', ['#,', 'x1']],
          ['V-BAR', ['V', 'love_V2'], ['#,', 'x2']]],
    vars=None,
    adj=[],
)

RULES_RGL = [
    tense_rule,
    le_Det,
    loi_Det,
    mi_Pron,
    do_Pron,
    je_J,
    ceho_J,
    koha_N,
    midju_V,
    san_francisco_PN,
    los_angeles_PN,
    san_diego_PN,
    san_jose_PN,
    california_PN,
    north_california_PN,
    kulnu_A,
    canja_A,
    jdini_A,
    xunre_V,
    xunre_A,
    blanu_A,
    moi_A,
    vo_A,
    lidne_A,
    xahugri_N,
    tcadu_V,
    prami_V,
]
