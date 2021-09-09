import unittest
from hamcrest import assert_that, equal_to
from transform.apply_templates import apply_templates
from transform.matchers import MatchName
from transform.transformers import Replace, TransformChildren
from transform.types import Rule


class ApplyTemplatesTest(unittest.TestCase):
    @staticmethod
    def test_id_transform():
        tree = ['something', ['quite', ['random']], ['just', ['for a smoke'], ['test']]]

        back = apply_templates([], tree)

        assert_that(list(back), equal_to([tree]))

    @staticmethod
    def test_substitute_subtree():
        tree = ['root', ['child', 'anything here', '234234'], ['sub', ['child', 'ignored']]]
        templates = [Rule(MatchName('child'), Replace([['new-child']]))]

        back = apply_templates(templates, tree)

        expected = ['root', ['new-child'], ['sub', ['new-child']]]
        assert_that(list(back), equal_to([expected]))

    @staticmethod
    def test_flatten_result():
        tree = ['a', ['a', ['a', ['b', 'c', 'd']]]]
        templates = [Rule(MatchName('a'), TransformChildren())]

        back = apply_templates(templates, tree)

        normalized = ['b', 'c', 'd']
        assert_that(list(back), equal_to([normalized]))


if '__main__' == __name__:
    unittest.main()