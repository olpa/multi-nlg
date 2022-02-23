import unittest
from hamcrest import assert_that, equal_to, instance_of, all_of, has_length

from mnlg.dtree.types import LcsToDtreeContext
from mnlg.dtree.functions import tag_clitic_indirect, to_spec, attach_adjunct
from mnlg.dtree.functions import lcs_adj_bar
from mnlg.dtree.rules_rgl import to_tense_tags
from lojban_xbar import lexp_to_tree


def mk_max(xtype: str, name: str):
    return [f'{xtype}-MAX', [f'{xtype}-BAR', [xtype, name]]]


lexp_n_max = mk_max('N', 'aaa')


class FunctionsTest(unittest.TestCase):

    @staticmethod
    def test_no_tags_to_present_simul():
        xmax = lexp_to_tree(['V-MAX', ['V-BAR', ['V', 'do']]])

        rlg_tags = to_tense_tags(xmax)

        assert_that(rlg_tags, equal_to([
            ['tag', 'Ant', 'ASimul'],
            ['tag', 'Tense', 'TPres'],
        ]))

    @staticmethod
    def test_past_simul():
        xmax = lexp_to_tree(['V-MAX', ['V-BAR', ['V', ['tag', 'pu'], 'do']]])

        rlg_tags = to_tense_tags(xmax)

        assert_that(rlg_tags, equal_to([
            ['tag', 'Ant', 'ASimul'],
            ['tag', 'Tense', 'TPast'],
        ]))

    @staticmethod
    def test_spec_with_xmax():
        tree = lexp_to_tree(
            ['D-MAX', ['D-SPEC', lexp_n_max], ['D-BAR', ['D', 'd']]])

        back = to_spec(tree)

        assert_that(back, all_of(instance_of(tuple), has_length(2)))
        func, lexp_xmax = back
        assert_that(func, equal_to('map'))
        assert_that(lexp_xmax, equal_to(lexp_n_max))

    @staticmethod
    def test_spec_with_tags():
        tags = [['tag', 't1'], ['tag', 't2', 'v2']]
        tree = lexp_to_tree(
            ['D-MAX', ['D-SPEC', *tags], ['D-BAR', ['D', 'd']]])

        back = to_spec(tree)

        assert_that(back, all_of(instance_of(tuple), has_length(2)))
        func, lexp_xspec = back
        assert_that(func, equal_to('node'))
        assert_that(lexp_xspec, equal_to(tags))

    @staticmethod
    def mk_nmax_lexp_with_tags(*tag):
        return ['N-MAX',
                ['N-SPEC'], ['N-BAR', ['N', *tag, 'aaa'],
                             ['N-MAX', ['N-BAR', ['N', 'bbb']]]]]

    @staticmethod
    def test_clitic_indirect():
        lexp = FunctionsTest.mk_nmax_lexp_with_tags()
        expected_clitic_lexp = FunctionsTest.mk_nmax_lexp_with_tags(
            ['tag', 'clitic', 'indirect'])

        clitic_lexp = tag_clitic_indirect(None, lexp)

        assert_that(clitic_lexp, equal_to(expected_clitic_lexp))

    @staticmethod
    def test_attach_adjunct_none():
        nbar = lexp_n_max[1]

        back = attach_adjunct(None, nbar, None)

        assert_that(back, equal_to(nbar))

    @staticmethod
    def test_attach_adjunct_nmax():
        base = ['V-FRAME', ['V', 'do_V']]

        back = attach_adjunct(None, base, lexp_n_max)

        assert_that(back, equal_to(['V-BAR', base, lexp_n_max]))

    @staticmethod
    def test_attach_adjunct_bar_without_adjunct():
        base = ['N-BAR', ['N', 'some_N']]

        back = attach_adjunct(None, base, base)

        assert_that(back, equal_to(base))

    @staticmethod
    def test_attach_adjunct_bar_with_one_adjunct():
        base = ['N-BAR', ['N', 'some_N']]
        adj_bar = ['N-BAR', base, lexp_n_max]

        back = attach_adjunct(None, base, adj_bar)

        assert_that(back, equal_to(
            ['N-BAR', ['N-BAR', ['N', 'some_N']], lexp_n_max]))

    @staticmethod
    def test_attach_adjunct_bar_with_several_adjuncts():
        base = ['N-BAR', ['N', 'some_N']]
        adj_bar = ['A-BAR',
                   ['A-BAR',
                    ['A-BAR',
                     ['A-BAR', ['A', 'dropped_A'], mk_max('N', 'dropped_N')],
                     mk_max('A', 'a1_A')],
                    mk_max('A', 'a2_A')],
                   mk_max('A', 'a3_A')]

        back = attach_adjunct(None, base, adj_bar)

        assert_that(back, equal_to(
            ['N-BAR',
             ['N-BAR',
              ['N-BAR',
               ['N-BAR', ['N', 'some_N']],
               mk_max('A', 'a1_A')],
              mk_max('A', 'a2_A')],
             mk_max('A', 'a3_A')]))

    @staticmethod
    def test_attach_adjunct_to_own_adjunct():
        base = ['N-BAR', ['N-BAR', ['N', 'some_N']], mk_max('A', 'own_A')]
        adj_bar = ['A-BAR',
                   ['A-BAR', ['A', 'dropped_A']],
                   mk_max('A', 'extra_A')]

        back = attach_adjunct(None, base, adj_bar)

        assert_that(back, equal_to(
            ['N-BAR',
             ['N-BAR',
              ['N-BAR', ['N', 'some_N']],
              mk_max('A', 'own_A')],
             mk_max('A', 'extra_A')]))

    # -

    lcs_to_dtree_context = LcsToDtreeContext(
        lcs_to_dtree=lambda _rules, tree, _xtype: tree.to_lexp(),
        rules=[],
    )

    @staticmethod
    def test_get_adj_bar():
        in_bar = ['A-MAX', ['A-BAR', ['A', 'red_A']]]
        lexp = ['N-MAX', ['N-BAR',
                          ['N-BAR', ['N', 'some_N']],
                          in_bar]]

        back = lcs_adj_bar(lexp_to_tree(lexp),
                           FunctionsTest.lcs_to_dtree_context)

        assert_that(back, equal_to(['A-BAR', in_bar]))

    @staticmethod
    def test_get_adj_bar_skip_imax():
        in_bar = ['A-MAX', ['A-BAR', ['A', 'red_A']]]
        lexp = ['N-MAX', ['N-BAR',
                          ['N-BAR', ['N', 'some_N']],
                          ['I-MAX', ['I-BAR', ['I'], in_bar]]]]

        back = lcs_adj_bar(lexp_to_tree(lexp),
                           FunctionsTest.lcs_to_dtree_context)

        assert_that(back, equal_to(['A-BAR', in_bar]))


if '__main__' == __name__:
    unittest.main()