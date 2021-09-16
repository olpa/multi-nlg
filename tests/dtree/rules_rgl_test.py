import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import to_tense_tags
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


if '__main__' == __name__:
    unittest.main()
