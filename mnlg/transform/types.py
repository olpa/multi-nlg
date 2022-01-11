from __future__ import annotations
import typing
from abc import abstractmethod, ABC

#
# Consider the structure:
# ```
#   ['node', 'child1', 'child2']
# ```
# It defines a node named 'node' with children 'child1' and 'child2'.
# Its type is: the first element is string, the rest are nodes.
#
# Actually, the correct definition should be:
# ```
#   ['node', ['child1'], ['child2']]
# ```
# But I've noticed that I often create "incorrect" trees because
# it's so convenient. Therefore, I've allowed the degenerative case
# of a node which is just a string.
#

TreeNode = typing.Union[str, typing.List[typing.Union[str, 'TreeNode']]]

NodeSet = typing.List[TreeNode]

IterableNodeSet = typing.Iterable[TreeNode]


#
# A-la XSLT and XPath
#

class Projector(ABC):
    """ From a context node to more nodes to continue """
    @abstractmethod
    def project(self, node: TreeNode) -> IterableNodeSet:
        raise NotImplementedError


class Matcher(ABC):
    """ Accept or reject a node candidate """
    @abstractmethod
    def is_match(self, node: TreeNode) -> bool:
        raise NotImplementedError


class Transformer(ABC):
    """ Rewrite the tree, likely using `apply-templates` recursively """
    @abstractmethod
    def transform(self, rules: list['Rule'], node: TreeNode) -> NodeSet:
        raise NotImplementedError


class Rule(typing.NamedTuple):
    """ Associate a transformation with a match """
    match: Matcher
    transform: Transformer
