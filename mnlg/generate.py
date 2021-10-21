import enum
import os
import typing
import camxes_py
import pgf

from mnlg.gf.stree_to_gf import stree_to_gf_fullstop
from mnlg.dtree import lcs_to_dtree
from mnlg.dtree.rules_en import RULES as RULES_EN
from mnlg.dtree.rules_es import RULES as RULES_ES
from mnlg.dtree.rules_de import RULES as RULES_DE
from mnlg.dtree.rules_ru import RULES as RULES_RU
from mnlg.dtree.rules_zh import RULES as RULES_ZH
from mnlg.lcs.camxes_to_lcs import camxes_to_lcs
from mnlg.xbar import lexp_to_tree
from mnlg.transform import TreeNode

PgfLang = object


class Step(enum.IntEnum):
    # Ordered steps, +1 and -1 bring to the next and prev steps
    lojban = 1
    parse = 2
    lcs = 3
    dtree = 4
    stree = 5
    gf = 6
    natural = 7


class ConversionArtefacts(typing.NamedTuple):
    lojban: str
    parse: TreeNode
    lcs: TreeNode
    dtree: TreeNode
    stree: TreeNode
    natural: str


class MnlgInit:
    def __init__(self, grammar_file_dir: str, grammar_name: str):
        pgf_file = os.path.join(grammar_file_dir, grammar_name + '.pgf')
        self.grammar_name = grammar_name
        self.grammar = pgf.readPGF(pgf_file)

    def get_grammar(self, lang: str):
        gf_names = {
            'en': 'Eng',
            'es': 'Spa',
            'de': 'Ger',
            'ru': 'Rus',
            'zh': 'Chi',
        }
        if lang not in gf_names:
            raise ValueError(f'Language not supported: {lang}')
        lang = gf_names[lang]
        return self.grammar.languages[self.grammar_name + lang]

    @staticmethod
    def get_rules(lang: str):
        rules = {
            'en': RULES_EN,
            'es': RULES_ES,
            'de': RULES_DE,
            'ru': RULES_RU,
            'zh': RULES_ZH,
        }
        if lang not in rules:
            raise ValueError(f'Language not supported: {lang}')
        return rules[lang]


def generate_one_sentence(
        mnlg: MnlgInit,
        interlingua: typing.Union[str, TreeNode],
        lang: str,
        begin_step: typing.Optional[Step] = Step.lojban,
        end_step: typing.Optional[Step] = Step.natural,
) -> typing.Union[str, TreeNode]:
    so_far = interlingua
    if begin_step <= Step.parse <= end_step:
        so_far = camxes_py.parse(so_far)
    if begin_step <= Step.lcs <= end_step:
        so_far = camxes_to_lcs(so_far)
    if begin_step <= Step.dtree <= end_step:
        rules = mnlg.get_rules(lang)
        lcs_tree = lexp_to_tree(so_far)
        so_far = lcs_to_dtree(rules, lcs_tree)
    if begin_step <= Step.gf <= end_step:
        stree = lexp_to_tree(so_far)
        so_far = stree_to_gf_fullstop(stree)
    if begin_step <= Step.natural <= end_step:
        grammar = mnlg.get_grammar(lang)
        if isinstance(so_far, str):  # input from command line
            so_far = pgf.readExpr(so_far)
        s = grammar.linearize(so_far)
        if 'zh' == lang:
            s = s.replace(' ', '')
        else:
            s = s[0].upper() + s[1:]
        if 'es' == lang:
            s = s.replace(' de el ', ' del ')
        so_far = s
    return so_far


def generate(mnlg: MnlgInit, interlingua: str) -> typing.Mapping[str, str]:
    lcs = generate_one_sentence(
        mnlg, interlingua, 'ignored', Step.lojban, Step.lcs
    )
    s_en = generate_one_sentence(mnlg, lcs, 'en', Step.dtree)
    s_es = generate_one_sentence(mnlg, lcs, 'es', Step.dtree)
    s_de = generate_one_sentence(mnlg, lcs, 'de', Step.dtree)
    s_ru = generate_one_sentence(mnlg, lcs, 'ru', Step.dtree)
    s_zh = generate_one_sentence(mnlg, lcs, 'zh', Step.dtree)
    return {
        'en': s_en,
        'es': s_es,
        'de': s_de,
        'ru': s_ru,
        'zh': s_zh,
    }
