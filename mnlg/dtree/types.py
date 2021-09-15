import typing

from mnlg.transform import TreeNode
from mnlg.xbar import XType


class Rule(typing.NamedTuple):
    x: XType
    head: typing.Optional[str]
    tree: TreeNode
    vars: typing.Optional[dict[str, typing.Union[str, typing.Callable[[TreeNode], TreeNode]]]]
