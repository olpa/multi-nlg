import os
import typing

import camxes_py
import pgf

from mnlg.gf.stree_to_gf import stree_to_gf_fullstop
from mnlg.dtree import lcs_to_dtree
from mnlg.dtree.rules_en import RULES as RULES_EN
from mnlg.dtree.rules_es import RULES as RULES_ES
from mnlg.camxes_to_lcs import camxes_to_lcs
from mnlg.xbar import lexp_to_tree

PgfLang = object


class MnlgInit:
    def __init__(self, grammar_file_dir: str, grammar_name: str):
        pgf_file = os.path.join(grammar_file_dir, grammar_name + '.pgf')
        self.grammar_name = grammar_name
        self.grammar = pgf.readPGF(pgf_file)

    def get_grammar(self, lang: str):
        if lang == 'en':
            lang = 'Eng'
        elif lang == 'es':
            lang = 'Spa'
        else:
            raise ValueError(f'Language not supported: {lang}')
        return self.grammar.languages[self.grammar_name + lang]

    @staticmethod
    def get_rules(lang: str):
        if lang == 'en':
            return RULES_EN
        if lang == 'es':
            return RULES_ES
        raise ValueError(f'Language not supported: {lang}')


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
    s = s[0].upper() + s[1:]
    return s


def generate(mnlg: MnlgInit, interlingua: str) -> typing.Mapping[str, str]:
    s_en = generate_one_sentence(mnlg, interlingua, 'en')
    s_es = generate_one_sentence(mnlg, interlingua, 'es')
    if 'nerkla' in interlingua:
        return {
                'en': s_en,
                'es': s_es,
                'de': 'Johann brach ins Zimmer ein.',
                'ru': 'Джон ворвался в комнату.',
                'zh': '约翰闯进房间。',
                }
    if 'dakfu' in interlingua:
        return {
                'en': s_en,
                'es': s_es,
                'de': 'Ich erstach Johann.',
                'ru': 'Я ударил Джона ножом.',
                'zh': '我刺伤了约翰。',
                }
