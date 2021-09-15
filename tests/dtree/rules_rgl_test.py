import unittest
from hamcrest import assert_that, equal_to

from mnlg.dtree.rules_rgl import to_tense_tags


class TenseTaggingTest(unittest.TestCase):

    @staticmethod
    def test_no_tags_to_present_simul():
        rlg_tags = to_tense_tags([])

        assert_that(rlg_tags, equal_to({
            'Tense': 'TPres',
            'Ant': 'ASimul',
        }))

    @staticmethod
    def test_past_simul():
        rlg_tags = to_tense_tags(['pu'])

        assert_that(rlg_tags, equal_to({
            'Tense': 'TPast',
            'Ant': 'ASimul',
        }))


if '__main__' == __name__:
    unittest.main()
