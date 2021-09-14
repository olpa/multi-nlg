import unittest
from hamcrest import assert_that, equal_to
from mnlg.transform import apply_templates, MatchName, Replace, Rule


class ApplyTemplatesTest(unittest.TestCase):
    @staticmethod
    def test_id_transform():
        tree = ['something', ['quite', ['random']],
                ['just', ['for a smoke'], ['test']]]

        back = apply_templates([], tree)

        assert_that(list(back), equal_to([tree]))

    @staticmethod
    def test_substitute_subtree():
        tree = ['root', ['child', 'anything here', '234234'],
                ['sub', ['child', 'ignored']]]
        templates = [Rule(MatchName('child'), Replace([['new-child']]))]

        back = apply_templates(templates, tree)

        expected = ['root', ['new-child'], ['sub', ['new-child']]]
        assert_that(list(back), equal_to([expected]))

    @staticmethod
    def test_visit_headless_nodes():
        tree = [[[['a', 'c', 'd'], 'k']]]
        templates = [Rule(MatchName('a'), Replace([['seen']]))]

        back = apply_templates(templates, tree)

        assert_that(list(back), equal_to([['seen'], 'k']))


if '__main__' == __name__:
    unittest.main()
