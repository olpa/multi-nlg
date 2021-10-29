import json
import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import tense_rule, je_J, \
    jdini_A, kulnu_A, canja_A
from mnlg.dtree.rules_en import RULES as RULES_EN
from mnlg.dtree.rules_rgl import RULES_RGL
from mnlg.dtree.rules_es import RULES as RULES_ES
from mnlg.dtree.rules_de import RULES as RULES_DE
from mnlg.dtree.rules_ru import RULES as RULES_RU
from mnlg.dtree.rules_zh import RULES as RULES_ZH
from mnlg.dtree import lcs_to_dtree, Rule
from mnlg.xbar import lexp_to_tree, XType, XMax
from tests.util.fixture import load_lcs, load_dtree

lexp_n_aaa = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
lexp_n_bbb = ['N-MAX', ['N-BAR', ['N', 'bbb']]]


class LcsToDtreeTest(unittest.TestCase):

    @classmethod
    def test_literal_subst_without_vars(cls):
        rules = [Rule(x=XType.N, head='aaa', tree=['bbb'], vars=None, adj=[],)]
        lcs = lexp_to_tree(lexp_n_aaa)

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(['bbb']))

    @classmethod
    def test_run_tag_function(cls):
        rules = [tense_rule]
        lcs = lexp_to_tree(['I-MAX', ['I-BAR', ['I', ['tag', 'pu']]]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['I-MAX', ['I-BAR',
                       ['I',
                        ['tag', 'Ant', 'ASimul'],
                        ['tag', 'Tense', 'TPast']]]]))

    @classmethod
    def test_subst_complement(cls):
        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['bbb'],
            vars=None,
            adj=[],)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [tense_rule, subst_rule]
        lcs = lexp_to_tree(['I-MAX', ['I-BAR', ['I'], n_max]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['I-MAX', ['I-BAR',
                       ['I',
                        ['tag', 'Ant', 'ASimul'],
                        ['tag', 'Tense', 'TPres']],
                       ['bbb']]]))

    b_to_some_rule = Rule(
        x=XType.N,
        head='bbb',
        tree=['some-bbb'],
        vars=None,
        adj=[],)

    c_to_some_rule = Rule(
        x=XType.N,
        head='ccc',
        tree=['some-ccc'],
        vars=None,
        adj=[],)

    @classmethod
    def test_subst_spec(cls):
        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['expect-bbb', ['#,', 'spec']],
            vars=None,
            adj=[],)
        n_max = ['N-MAX', ['N-BAR', ['N', 'bbb']]]
        rules = [LcsToDtreeTest.b_to_some_rule, subst_rule]
        lcs = lexp_to_tree(
            ['N-MAX', ['N-SPEC', n_max], ['N-BAR', ['N', 'aaa']]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(['expect-bbb', ['some-bbb']]))

    @classmethod
    def test_subst_x1(cls):
        subst_rule = Rule(
            x=XType.V,
            head='aaa',
            tree=['expect-bbb', ['#,', 'x1']],
            vars=None,
            adj=[],)
        n_max = ['N-MAX', ['N-BAR', ['N', 'bbb']]]
        rules = [LcsToDtreeTest.b_to_some_rule, subst_rule]
        lcs = lexp_to_tree(['V-MAX', ['V-BAR', ['V', 'aaa'], n_max]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(['expect-bbb', ['some-bbb']]))

    @classmethod
    def test_copy_spec_and_x(cls):
        n_max_spec = ['N-MAX', ['N-BAR', ['N', 'n-spec']]]
        n_max_x2 = ['N-MAX', ['N-BAR', ['N', 'n-x2']]]
        lcs = lexp_to_tree(
            ['V-MAX', ['V-SPEC', n_max_spec],
             ['V-FRAME', ['V', 'v-test'], lexp_n_aaa, n_max_x2]])
        subst_rule = Rule(
            x=XType.V,
            head='v-test',
            vars=None,
            tree=[['a', ['#,', 'copy-spec']], ['b', ['#,', 'copy-x2']]],
            adj=[],
        )

        dtree = lcs_to_dtree([subst_rule], lcs)

        assert_that(dtree, equal_to([['a', n_max_spec], ['b', n_max_x2]]))

    @classmethod
    def test_rescan_returned_tree(cls):
        lcs = lexp_to_tree(['N-MAX', ['N-SPEC', ['tag', 'some-tag']],
                            ['N-BAR', ['N', 'name']]])
        rescan_rule = Rule(
            x=XType.N,
            head='name',
            vars=None,
            tree=['#,lcs', ['N-MAX',
                  ['#,', 'copy-spec'], ['N-BAR', ['N', 'name2']]]],
            adj=[],
        )
        subst_rule = Rule(
            x=XType.N,
            head='name2',
            vars=None,
            tree=['#,', 'copy-spec'],
            adj=[],
        )

        dtree = lcs_to_dtree([rescan_rule, subst_rule], lcs)

        assert_that(dtree, equal_to(['X-SPEC', ['tag', 'some-tag']]))

    @staticmethod
    def test_subst_in_returned_tree():
        lcs = lexp_to_tree(
            ['N-MAX', ['N-SPEC', ['tag', 'from-spec']],
             ['N-BAR', ['N', 'aaa']]])

        def subst_func(_lcs):
            return ['subst', ['#,', 'copy-spec']]

        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['#,', 'subst-func'],
            vars={'subst-func': subst_func},
            adj=[],
        )

        dtree = lcs_to_dtree([subst_rule], lcs)

        assert_that(dtree, equal_to(['X-SPEC', ['tag', 'from-spec']]))

    # --

    @staticmethod
    def wrap_with_d(det_tag: str, lexp_n):
        return ['D-MAX', ['D-BAR',
                          ['D', det_tag],
                          lexp_n]]

    @staticmethod
    def test_determiner():
        lcs = lexp_to_tree(LcsToDtreeTest.wrap_with_d('le', lexp_n_aaa))

        dtree = lcs_to_dtree(RULES_EN, lcs)

        assert_that(dtree, equal_to(
            ['D-MAX', ['D-BAR', ['D',
                                 ['tag', 'Num', 'NumSg'],
                                 ['tag', 'Quant', 'DefArt'],
                                 ], ['TODO(no_rule_N-MAX<aaa>)']]]))
    # --

    manner_rule = Rule(
        x=XType.V,
        head='do',
        vars=None,
        tree=['#,', 'manner-x3'],
        adj=[],
    )

    manner_dtree = ['D-MAX',
                    ['D-BAR',
                     ['D', 'loi'],
                     ['N-MAX', ['N-BAR',
                                ['N', ['tag', 'manner', 'x3'], 'do']]]]]

    @classmethod
    def test_manner_meaning(cls):
        lexp = ['V-MAX', ['V-FRAME', ['V', 'do'],
                          ['N-MAX', ['N-BAR', ['N', 'x1']]],
                          ['N-MAX', ['N-BAR', ['N', 'x2']]],
                          ['N-MAX', ['N-BAR', ['N', 'x3']]],
                          ]]
        lcs = lexp_to_tree(lexp)

        dtree = lcs_to_dtree([LcsToDtreeTest.manner_rule], lcs)

        assert_that(dtree, equal_to(LcsToDtreeTest.manner_dtree))

    @classmethod
    def test_manner_meaning_with_det(cls):
        lexp = ['V-MAX', ['V-FRAME', ['V', 'do'],
                          ['N-MAX', ['N-BAR', ['N', 'x1']]],
                          ['N-MAX', ['N-BAR', ['N', 'x2']]],
                          ['D-MAX', ['D-BAR', ['D', ['tag', 'le']],
                                     ['N-MAX', ['N-BAR', ['N', 'x3']]]]],
                          ]]
        lcs = lexp_to_tree(lexp)

        dtree = lcs_to_dtree([LcsToDtreeTest.manner_rule], lcs)

        assert_that(dtree, equal_to(LcsToDtreeTest.manner_dtree))

    @classmethod
    def test_from_manner_to_n(cls):
        lcs = lexp_to_tree(
            ['N-MAX', ['N-BAR', ['N', ['tag', 'manner', 'int'], 'ext']]])

        dtree = lcs_to_dtree([], lcs)

        assert_that(dtree, equal_to(['N-MAX', ['N-BAR', ['N', 'ext_int_CN']]]))

    # -

    @staticmethod
    def test_add_adjunct():
        rules = [Rule(
            x=XType.N,
            head='aaa',
            tree=lexp_n_aaa,
            vars=None,
            adj=[lexp_n_bbb, lexp_n_aaa])]

        dtree = lcs_to_dtree(rules, lexp_to_tree(lexp_n_aaa))

        assert_that(dtree, equal_to(
            ['N-MAX', ['N-BAR',
                       ['N-BAR',
                        ['N-BAR', ['N', 'aaa']],
                        lexp_n_bbb],
                       lexp_n_aaa]]))

    @staticmethod
    def test_call_func_with_arg():
        rules = [Rule(
            x=XType.N,
            head='aaa',
            tree=['#,', 'tag-clitic-indirect', lexp_n_bbb],
            vars=None,
            adj=[])]

        dtree = lcs_to_dtree(rules, lexp_to_tree(lexp_n_aaa))

        assert_that(dtree, equal_to(
            ['N-MAX', ['N-BAR', ['N', ['tag', 'clitic', 'indirect'], 'bbb']]]))

    @staticmethod
    def test_expand_arguments_to_function():
        seen_by_function = None

        def function(lcs: XMax, args):
            nonlocal seen_by_function
            seen_by_function = args
            return lcs.to_lexp()

        rules = [Rule(
            x=XType.N,
            head='aaa',
            tree=['#,', 'function'],
            vars={
                'function': [function, ['#,', 'spec']],
            },
            adj=[],
        )]
        lcs = lexp_to_tree(
            ['N-MAX', ['N-SPEC', ['tag', 'name', 'value']],
             ['N-BAR', ['N', 'aaa']]])

        lcs_to_dtree(rules, lcs)

        assert_that(seen_by_function, equal_to([['tag', 'name', 'value']]))

    @staticmethod
    def test_nested_adjunct():
        rules = [Rule(
            x=XType.N,
            head='aaa',
            tree=['N-MAX',
                  ['#,', 'adjunct',
                   ['#,', 'adjunct',
                    ['N-BAR', ['N', 'in_nested_N']],
                    lexp_n_aaa],
                   lexp_n_bbb]],
            vars=None,
            adj=[])]

        dtree = lcs_to_dtree(rules, lexp_to_tree(lexp_n_aaa))

        assert_that(dtree, equal_to(
            ['N-MAX',
             ['N-BAR',
              ['N-BAR',
               ['N-BAR',
                ['N', 'in_nested_N']],
               lexp_n_aaa],
              lexp_n_bbb]]))

    @staticmethod
    def test_adj_bar_to_adj():
        rules = [
            Rule(
                x=XType.N,
                head='aaa',
                tree=['#,', 'lcs-adj-bar'],
                vars=None,
                adj=[]),
            Rule(
                x=XType.A,
                head='bbb',
                tree=['X-MAX', 'as_adj'],
                vars=None,
                adj=[])
        ]
        tree = lexp_to_tree(
            ['N-MAX',
             ['N-BAR',
              ['N-BAR',
               ['N-BAR', ['N', 'aaa']],
               lexp_n_bbb],
              lexp_n_bbb]])

        dtree = lcs_to_dtree(rules, tree)

        assert_that(dtree, equal_to(
            ['A-BAR', ['A-BAR', ['X-MAX', 'as_adj']], ['X-MAX', 'as_adj']]))

    @staticmethod
    def test_regression_j_with_adjunct():
        # kulnu je canja je jdini
        s_lexp_tree = '''["J-MAX", ["J-BAR", ["J-BAR", ["J-BAR",
        ["J", ["tag", "elide"], "je"],
        ["N-MAX", ["N-BAR", ["N", "kulnu"]]]], ["J-MAX", ["J-BAR", ["J",
        "je"], ["N-MAX", ["N-BAR", ["N", "canja"]]]]]], ["J-MAX", ["J-BAR",
         ["J", "je"], ["N-MAX", ["N-BAR", ["N", "jdini"]]]]]]]'''
        tree = lexp_to_tree(json.loads(s_lexp_tree))
        rules = [je_J, kulnu_A, canja_A, jdini_A]

        dtree = lcs_to_dtree(rules, tree)

        s_dtree = '''["J-MAX", ["J-BAR", ["J-BAR", ["J-BAR",
        ["J", ["tag", "elide"], "je"],
        ["A-MAX", ["A-BAR", ["A", "cultural_A"]]]], ["J-MAX", ["J-BAR",
        ["J", "je"], ["A-MAX", ["A-BAR", ["A", "commercial_A"]]]]]],
        ["J-MAX", ["J-BAR", ["J", "je"], ["A-MAX", ["A-BAR", ["A",
        "financial_A"]]]]]]]'''
        expected_dtree = json.loads(s_dtree)
        assert_that(dtree, equal_to(expected_dtree))

    @staticmethod
    def test_self_lcs_rescan():
        tree = lexp_to_tree(['V-MAX', ['V-FRAME', ['V', 'xunre']]])
        rescan_rule = Rule(
            x=XType.V,
            head='xunre',
            vars=None,
            tree=['#,lcs', ['#,', 'self'], 'A'],
            adj=[],
        )

        dtree = lcs_to_dtree([rescan_rule, *RULES_RGL], tree)

        assert_that(dtree, equal_to(['A-MAX', ['A-BAR', ['A', 'red_A']]]))

    @staticmethod
    def test_retain_xtype_in_conjunction():
        tree = lexp_to_tree(['J-MAX', ['J-BAR', ['J', "ce'o"],
                                       ['N-MAX', ['N-BAR', ['N', 'mi']]]]])

        dtree = lcs_to_dtree(RULES_RGL, tree)

        assert_that(dtree, equal_to(
            ['J-MAX', ['J-BAR', ['J', "ce'o"],
                       ['N-MAX',
                        ['N-BAR', ['N', ['tag', 'pron'], 'i_Pron']]]]]))

    @staticmethod
    def test_copy_tags():
        tree = lexp_to_tree(
            ['N-MAX', ['N-BAR', ['N',
                                 ['tag', 'tag1', 'val1'],
                                 ['tag', 'tag2'], 'some_N']]])
        tag_copy_rule = Rule(
            x=XType.N,
            head='some_N',
            vars=None,
            tree=['#,', 'tags'],
            adj=[],
        )

        dtree = lcs_to_dtree([tag_copy_rule], tree)

        assert_that(dtree, equal_to(
            [['tag', 'tag1', 'val1'], ['tag', 'tag2']]))


class LcsToDtreeExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lcs = load_lcs()
        cls.dtree = load_dtree()

    def do_lcs_test(self, rules, code_name, lang):
        source_lcs = lexp_to_tree(self.lcs[code_name])
        expected_dtree = self.dtree[f'{code_name}_{lang}']

        dtree = lcs_to_dtree(rules, source_lcs)

        assert_that(dtree, equal_to(expected_dtree))

    def test_break_forzar_en(self):
        self.do_lcs_test(RULES_EN, 'break_forzar', 'en')

    def test_stab_dar_en(self):
        self.do_lcs_test(RULES_EN, 'stab_dar', 'en')

    def test_break_forzar_es(self):
        self.do_lcs_test(RULES_ES, 'break_forzar', 'es')

    def test_stab_dar_es(self):
        self.do_lcs_test(RULES_ES, 'stab_dar', 'es')

    def test_break_forzar_de(self):
        self.do_lcs_test(RULES_DE, 'break_forzar', 'de')

    def test_stab_dar_de(self):
        self.do_lcs_test(RULES_DE, 'stab_dar', 'de')

    def test_break_forzar_ru(self):
        self.do_lcs_test(RULES_RU, 'break_forzar', 'ru')

    def test_stab_dar_ru(self):
        self.do_lcs_test(RULES_RU, 'stab_dar', 'ru')

    def test_break_forzar_zh(self):
        self.do_lcs_test(RULES_ZH, 'break_forzar', 'zh')

    def test_stab_dar_zh(self):
        self.do_lcs_test(RULES_ZH, 'stab_dar', 'zh')


if '__main__' == __name__:
    unittest.main()
