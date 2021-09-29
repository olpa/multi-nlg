import unittest
from hamcrest import assert_that, equal_to, instance_of, all_of, has_length

from mnlg.dtree.functions import tag_clitic_indirect, to_spec
from mnlg.dtree.rules_rgl import to_tense_tags, to_det_tags
from mnlg.xbar import lexp_to_tree

lexp_n_max = ['N-MAX', ['N-BAR', ['N', 'aaa']]]


class TenseTaggingTest(unittest.TestCase):

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
    def test_det_default():
        xmax = lexp_to_tree(['D-MAX', ['D-BAR', ['D']]])

        rlg_tags = to_det_tags(xmax)

        assert_that(rlg_tags, equal_to([
            ['tag', 'Num', 'NumSg'],
            ['tag', 'Quant', 'IndefArt'],
        ]))

    @staticmethod
    def test_det_tags():
        xmax = lexp_to_tree(['D-MAX', ['D-BAR', ['D', ['tag', 'le']]]])

        rlg_tags = to_det_tags(xmax)

        assert_that(rlg_tags, equal_to([
            ['tag', 'Num', 'NumSg'],
            ['tag', 'Quant', 'DefArt'],
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
    def test_clitic_indirect():
        def mk_nmax_lexp_with_tags(*tag):
            return ['N-MAX',
                    ['N-SPEC'], ['N-BAR', ['N', *tag, 'aaa'],
                                 ['N-MAX', ['N-BAR', ['N', 'bbb']]]]]
        lexp = mk_nmax_lexp_with_tags()
        expected_clitic_lexp = mk_nmax_lexp_with_tags(
            ['tag', 'clitic', 'indirect'])

        clitic_lexp = tag_clitic_indirect(None, lexp)

        assert_that(clitic_lexp, equal_to(expected_clitic_lexp))


if '__main__' == __name__:
    unittest.main()
