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
from mnlg.camxes_to_lcs import camxes_to_lcs
from mnlg.xbar import lexp_to_tree

PgfLang = object


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


def generate_one_sentence(mnlg: MnlgInit, interlingua: str, lang: str) -> str:
    rules = mnlg.get_rules(lang)
    grammar = mnlg.get_grammar(lang)
    camxes_lexp = camxes_py.parse(interlingua)
    lcs_lexp = camxes_to_lcs(camxes_lexp)
    lcs = lexp_to_tree(lcs_lexp)
    dtree_lexp = lcs_to_dtree(rules, lcs)
    dtree = lexp_to_tree(dtree_lexp)
    stree = dtree
    gf = stree_to_gf_fullstop(stree)
    s = grammar.linearize(gf)
    if 'zh' == lang:
        s = s.replace(' ', '')
    else:
        s = s[0].upper() + s[1:]
    return s


def generate(mnlg: MnlgInit, interlingua: str) -> typing.Mapping[str, str]:
    s_en = generate_one_sentence(mnlg, interlingua, 'en')
    s_es = generate_one_sentence(mnlg, interlingua, 'es')
    s_de = generate_one_sentence(mnlg, interlingua, 'de')
    s_ru = generate_one_sentence(mnlg, interlingua, 'ru')
    s_zh = generate_one_sentence(mnlg, interlingua, 'zh')
    return {
        'en': s_en,
        'es': s_es,
        'de': s_de,
        'ru': s_ru,
        'zh': s_zh,
    }
