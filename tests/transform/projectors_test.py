import unittest
from hamcrest import assert_that, equal_to

from mnlg.transform import MatchName, DeepDive


class DeepDiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.diver = DeepDive(MatchName('child'))

    def test_find_on_first_level(self):
        tree = ['root', ['child']]

        back = self.diver.project(tree)

        assert_that(list(back), equal_to([['child']]))

    def test_find_on_second_level(self):
        tree = ['root', ['child', ['child', 'level2']]]

        back = self.diver.project(tree)

        assert_that(list(back), equal_to([['child', 'level2']]))

    def test_find_several_on_deep_level(self):
        tree = ['root', ['child',
                         ['child', ['level2'],
                          ['child', ['level3']],
                          ['child', ['child', 'levelN']]]]]

        back = self.diver.project(tree)

        assert_that(list(back), equal_to(
            [['child', ['level3']], ['child', 'levelN']]))

    def test_stop_dive_on_mismatch(self):
        tree = ['root', ['child', ['stop-dive', ['child', 'nested']]]]

        back = self.diver.project(tree)

        assert_that(list(back), equal_to(
            [['child', ['stop-dive', ['child', 'nested']]]]))

    def test_dive_on_headless_nodes(self):
        tree = [[['child', [[['child', ['child', ['x', 'aaa']]]]]]]]

        back = self.diver.project(tree)

        assert_that(list(back), equal_to(
            [['child', ['x', 'aaa']]]))


if '__main__' == __name__:
    unittest.main()
