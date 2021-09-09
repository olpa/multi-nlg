import functools
import typing
from .nodeset import to_node_set, flatten_node_sets
from .projectors import Children
from .matchers import MatchAlways
from .types import TreeNode, NodeSet, Matcher, Projector, IterableNodeSet


class SelectStep(Projector):
    def __init__(self,
                 fop1: typing.Union[Matcher, Projector] = None,
                 fop2: typing.Union[Matcher, Projector] = None):
        self.matcher = MatchAlways()
        self.projector = Children()

        def use_arg(fop):
            if isinstance(fop, Matcher):
                self.matcher = fop
            elif isinstance(fop, Projector):
                self.projector = fop
            elif fop is None:
                pass
            else:
                raise TypeError('SelectStep: expecting "Matcher"'
                                ' or "Projector", got: ' + str(type(fop)))
        use_arg(fop1)
        use_arg(fop2)

    def project(self, node: TreeNode) -> IterableNodeSet:
        return filter(
            lambda kid: self.matcher.is_match(kid),
            self.projector.project(node)
        )


def select(tree: typing.Union[TreeNode, IterableNodeSet],
           path: list[Projector]) -> NodeSet:
    return list(functools.reduce(
        lambda nodes, step: flatten_node_sets(map(step.project, nodes)),
        path,
        to_node_set(tree)
    ))
