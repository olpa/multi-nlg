import unittest
from hamcrest import assert_that, equal_to

from mnlg.transform import Children, Projector, TreeNode, IterableNodeSet
from mnlg.transform import MatchName, SelectStep, select, SelectStepNorm

tree = ['tree', ['child1', 'a'], ['child2', 'b'], ['child1', 'c'],
        ['child2', ['sub-child2', 'd']], ['child2']]


class EachSecondChild(Projector):
    def project(self, node: TreeNode) -> IterableNodeSet:
        children = Children().project(node)
        return children[::2]


class SelectTest(unittest.TestCase):

    @staticmethod
    def test_return_same_if_no_select():
        back = select(tree, [])

        assert_that(list(back), equal_to([tree]))

    @staticmethod
    def test_by_default_return_children():
        back = select(tree, [SelectStep()])

        assert_that(list(back), equal_to(tree[1:]))

    @staticmethod
    def test_apply_to_node_set():
        back = select([tree, tree], [SelectStep()])

        assert_that(list(back), equal_to([*tree[1:], *tree[1:]]))

    @staticmethod
    def test_filter_nodes():
        back = select(tree, [SelectStep(MatchName('child1'))])

        assert_that(list(back), equal_to([['child1', 'a'], ['child1', 'c']]))

    @staticmethod
    def test_project_nodes():
        back = select(tree, [SelectStep(EachSecondChild())])

        assert_that(list(back), equal_to([['child1', 'a'],
                                          ['child1', 'c'], ['child2']]))

    @staticmethod
    def test_project_and_filter():
        back = select(tree, [SelectStep(EachSecondChild(),
                                        MatchName('child2'))])

        assert_that(list(back), equal_to([['child2']]))

    @staticmethod
    def test_several_steps():
        back = select(tree, [SelectStep(MatchName('child2')),
                             SelectStep(MatchName('sub-child2'))])

        assert_that(list(back), equal_to([['sub-child2', 'd']]))

    @staticmethod
    def test_camxes_tree():
        ctree = [['time', [['time_offset', 'etc']]]]
        back = select(ctree, [SelectStepNorm(MatchName('time_offset'))])

        assert_that(list(back), equal_to([['time_offset', 'etc']]))


if '__main__' == __name__:
    unittest.main()
