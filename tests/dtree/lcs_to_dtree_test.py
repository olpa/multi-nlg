import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import tense_rule
from mnlg.dtree.rules_en import RULES as RULES_EN, darxi_V
from mnlg.dtree.rules_es import RULES as RULES_ES
from mnlg.dtree import lcs_to_dtree, Rule
from mnlg.xbar import lexp_to_tree, XType, XSpecTag
from tests.util.fixture import load_lcs, load_dtree


class LcsToDtreeTest(unittest.TestCase):

    @classmethod
    def test_literal_subst_without_vars(cls):
        rules = [Rule(x=XType.N, head='aaa', tree=['bbb'], vars=None)]
        lcs = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'aaa']]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(['bbb']))

    @classmethod
    def test_run_tag_function(cls):
        rules = [tense_rule]
        lcs = lexp_to_tree(['I-MAX', ['I-BAR', ['I', None, ['tag', 'pu']]]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['I-MAX', ['I-BAR',
                       ['I', None,
                        ['tag', 'Ant', 'ASimul'],
                        ['tag', 'Tense', 'TPast']]]]))

    @classmethod
    def test_subst_complement(cls):
        subst_rule = Rule(x=XType.N, head='aaa', tree=['bbb'], vars=None)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [tense_rule, subst_rule]
        lcs = lexp_to_tree(['I-MAX', ['I-BAR', None, n_max]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['I-MAX', ['I-BAR',
                       ['I', None,
                        ['tag', 'Ant', 'ASimul'],
                        ['tag', 'Tense', 'TPres']],
                       ['bbb']]]))

    @classmethod
    def test_subst_spec(cls):
        subst_rule = Rule(x=XType.N, head='aaa', tree=['bbb'], vars=None)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [darxi_V, subst_rule]
        lcs = lexp_to_tree(
            ['V-MAX', ['V-SPEC', n_max], ['V-BAR', ['V', 'darxi']]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['V-MAX', ['V-SPEC', ['bbb']], ['V-BAR', ['V', 'stab_V2']]]))

    @classmethod
    def test_subst_x1(cls):
        subst_rule = Rule(x=XType.N, head='aaa', tree=['bbb'], vars=None)
        n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]
        rules = [darxi_V, subst_rule]
        lcs = lexp_to_tree(['V-MAX', ['V-BAR', ['V', 'darxi'], n_max]])

        dtree = lcs_to_dtree(rules, lcs)

        assert_that(dtree, equal_to(
            ['V-MAX', ['V-SPEC'], ['V-BAR', ['V', 'stab_V2'], ['bbb']]]))

    @classmethod
    def test_copy_spec_and_x(cls):
        n_max_spec = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'n-spec']]])
        n_max_x2 = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'n-x2']]])
        lcs = lexp_to_tree(['V-MAX', ['V-SPEC', n_max_spec],
                            ['V-FRAME', ['V', 'v-test'], n_max_x2]])
        subst_rule = Rule(
            x=XType.V,
            head='v-test',
            vars=None,
            tree=[['a', '#,', 'copy-spec'], ['b', '#,', 'copy-x2']]
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
                  'copy-spec', ['N-BAR', ['N', 'name2']]]
        )
        subst_rule = Rule(
            x=XType.N,
            head='name2',
            vars=None,
            tree=['#,', 'copy-spec']
        )

        dtree = lcs_to_dtree([rescan_rule, subst_rule], lcs)

        assert_that(dtree, equal_to([XSpecTag({'some-tag': 'some-tag'})]))


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


if '__main__' == __name__:
    unittest.main()
