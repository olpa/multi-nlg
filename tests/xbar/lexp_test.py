import typing
import unittest
from hamcrest import assert_that, equal_to, instance_of, none, not_none

from mnlg.xbar import lexp_to_tree, XHead, XType, XMax, XBarBase, XSpecTag
from mnlg.xbar import XBarFrame


class LexpTest(unittest.TestCase):

    @staticmethod
    def test_load_n():
        tree: XHead = lexp_to_tree(['N', 'some'])

        assert_that(typing.cast(object, tree), instance_of(XHead))
        assert_that(tree.type, equal_to(XType.N))
        assert_that(tree.s, equal_to('some'))
        assert_that(tree.tags, none())

    @staticmethod
    def test_load_tag():
        tree: XHead = lexp_to_tree(
            ['N', 'some', ['tag', 'some_tag', 'tag_value']])

        assert_that(tree.tags, not_none())
        assert_that(tree.tags, equal_to({'some_tag': 'tag_value'}))

    @staticmethod
    def test_set_tag_value_to_name():
        tree: XHead = lexp_to_tree(['N', 'some', ['tag', 'some_tag']])

        assert_that(tree.tags, equal_to({'some_tag': 'some_tag'}))

    @staticmethod
    def test_load_several_tags():
        tree: XHead = lexp_to_tree(
            ['N', 'some', ['tag', 'tag1'], ['tag', 'tag2'], ['tag', 'tag3']])

        assert_that(tree.tags, equal_to(
            {'tag1': 'tag1', 'tag2': 'tag2', 'tag3': 'tag3'}))

    n_bar = ['N-BAR', ['N', 'some_n']]
    v_bar = ['V-BAR', ['V', 'some_v']]

    def test_load_xmax(self):
        tree: XMax = lexp_to_tree(['N-MAX', self.n_bar])

        assert_that(typing.cast(object, tree), instance_of(XMax))
        assert_that(tree.type, equal_to(XType.N))
        xbar: XBarBase = tree.xbar
        assert_that(typing.cast(object, xbar), instance_of(XBarBase))
        assert_that(xbar.type, equal_to(XType.N))
        xhead: XHead = xbar.head
        assert_that(typing.cast(object, xhead), instance_of(XHead))
        assert_that(xhead.type, equal_to(XType.N))

    def test_drop_empty_spec(self):
        tree: XMax = lexp_to_tree(['N-MAX', ['N-SPEC'], self.n_bar])

        assert_that(tree.spec, none())

    def test_load_spec_as_xmax(self):
        tree: XMax = lexp_to_tree(
            ['V-MAX', ['V-SPEC', ['N-MAX', self.n_bar]], self.v_bar])

        assert_that(typing.cast(object, tree.spec), instance_of(XMax))

    def test_load_spec_as_tags(self):
        tree: XMax = lexp_to_tree(
            ['V-MAX', ['V-SPEC', ['tag', 'tag1'],
                       ['tag', 'tag2', 'val2']], self.v_bar])

        assert_that(typing.cast(object, tree.spec), instance_of(XSpecTag))
        assert_that(tree.spec.tags, equal_to({'tag1': 'tag1', 'tag2': 'val2'}))

    @staticmethod
    def test_load_headless_bar():
        tree: XBarBase = lexp_to_tree(['I-BAR'])

        assert_that(typing.cast(object, tree), instance_of(XBarBase))
        assert_that(typing.cast(object, tree.head), instance_of(XHead))
        assert_that(tree.head.s, none())

    @staticmethod
    def test_load_head_with_tags():
        tree: XHead = lexp_to_tree(['N', ['tag', 'tagN1'],
                                    'name_n', ['tag', 'tagN2', 'valN2']])

        assert_that(tree.tags, equal_to({'tagN1': 'tagN1', 'tagN2': 'valN2'}))

    @staticmethod
    def test_load_v_frame():
        tree: XBarFrame = lexp_to_tree(['V-FRAME', ['V', 'some_v']])

        assert_that(typing.cast(object, tree), instance_of(XBarFrame))
        assert_that(tree.head.s, equal_to('some_v'))


if '__main__' == __name__:
    unittest.main()
