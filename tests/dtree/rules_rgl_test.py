import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import to_tense_tags, to_det_tags
from mnlg.xbar import lexp_to_tree


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


if '__main__' == __name__:
    unittest.main()
