import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import tense_rule
from mnlg.dtree.rules_en import RULES as RULES_EN, darxi_V
from mnlg.dtree.rules_es import RULES as RULES_ES
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

    @classmethod
    def test_subst_spec(cls):
        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['bbb'],
            vars=None,
            adj=[],)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [darxi_V, subst_rule]
        lcs = lexp_to_tree(
            ['V-MAX', ['V-SPEC', n_max], ['V-BAR', ['V', 'darxi']]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['V-MAX', ['V-SPEC', ['bbb']], ['V-BAR', ['V', 'stab_V2']]]))

    @classmethod
    def test_subst_x1(cls):
        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['bbb'],
            vars=None,
            adj=[],)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [darxi_V, subst_rule]
        lcs = lexp_to_tree(['V-MAX', ['V-BAR', ['V', 'darxi'], n_max]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['V-MAX', ['V-SPEC'], ['V-BAR', ['V', 'stab_V2'], ['bbb']]]))

    @classmethod
    def test_copy_spec_and_x(cls):
        n_max_spec = ['N-MAX', ['N-BAR', ['N', 'n-spec']]]
        n_max_x2 = ['N-MAX', ['N-BAR', ['N', 'n-x2']]]
        lcs = lexp_to_tree(['V-MAX', ['V-SPEC', n_max_spec],
                            ['V-FRAME', ['V', 'v-test'], n_max_x2]])
        subst_rule = Rule(
            x=XType.V,
            head='v-test',
            vars=None,
            tree=[['a', '#,', 'copy-spec'], ['b', '#,', 'copy-x2']],
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
            tree=['#,lcs', 'N-MAX', '#,',
                  'copy-spec', ['N-BAR', ['N', 'name2']]],
            adj=[],
        )
        subst_rule = Rule(
            x=XType.N,
            head='name2',
            vars=None,
            tree=['#,@', 'copy-spec'],
            adj=[],
        )

        dtree = lcs_to_dtree([rescan_rule, subst_rule], lcs)

        assert_that(dtree, equal_to(['X-SPEC', ['tag', 'some-tag']]))

    @staticmethod
    def test_subst_in_returned_tree():
        lcs = lexp_to_tree(
            ['N-MAX', ['N-SPEC', ['tag', 'from-spec']],
             ['N-BAR', ['N', 'aaa']]])

        def subst_func(lcs):
            return ['subst', ['#,@', 'copy-spec']]

        subst_rule = Rule(
            x=XType.N,
            head='aaa',
            tree=['#,@', 'subst-func'],
            vars={'subst-func': subst_func},
            adj=[],
        )

        dtree = lcs_to_dtree([subst_rule], lcs)

        assert_that(dtree, equal_to(['X-SPEC', ['tag', 'from-spec']]))

    # --

    @staticmethod
    def wrap_with_d(det_tag: str, lexp_n):
        return ['D-MAX', ['D-BAR',
                          ['D', ['tag', det_tag]],
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
        tree=['#,@', 'manner-x3'],
        adj=[],
    )

    manner_dtree = ['D-MAX',
                    ['D-BAR',
                     ['D', ['tag', 'loi']],
                     ['N-MAX', ['N-BAR',
                                ['N', ['tag', 'manner', 'x3'], 'do']]]]]

    @classmethod
    def test_manner_meaning(cls):
        lexp = ['V-MAX', ['V-FRAME', ['V', 'do'],
                          ['N-MAX', ['N-BAR', ['N', 'x2']]],
                          ['N-MAX', ['N-BAR', ['N', 'x3']]],
                          ]]
        lcs = lexp_to_tree(lexp)

        dtree = lcs_to_dtree([LcsToDtreeTest.manner_rule], lcs)

        assert_that(dtree, equal_to(LcsToDtreeTest.manner_dtree))

    @classmethod
    def test_manner_meaning_with_det(cls):
        lexp = ['V-MAX', ['V-FRAME', ['V', 'do'],
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

        assert_that(dtree, equal_to(['N-MAX', ['N-BAR', ['N', 'ext_int_N']]]))

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
            tree=['#,@', ['tag-clitic-indirect', lexp_n_bbb]],
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
            tree=['#,@', 'function'],
            vars={
                'function': [function, '#,@', 'spec'],
            },
            adj=[],
        )]
        lcs = lexp_to_tree(
            ['N-MAX', ['N-SPEC', ['tag', 'name', 'value']],
             ['N-BAR', ['N', 'aaa']]])

        lcs_to_dtree(rules, lcs)

        assert_that(seen_by_function, equal_to(['tag', 'name', 'value']))


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

    def test_break_forzar(self):
        self.do_lcs_test(RULES_EN, 'break_forzar', 'en')

    def test_stab_dar_en(self):
        self.do_lcs_test(RULES_EN, 'stab_dar', 'en')

    def test_break_forzar_es(self):
        self.do_lcs_test(RULES_ES, 'break_forzar', 'es')

    def test_stab_dar_es(self):
        self.do_lcs_test(RULES_ES, 'stab_dar', 'es')


if '__main__' == __name__:
    unittest.main()
