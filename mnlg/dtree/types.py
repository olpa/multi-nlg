import typing

from mnlg.transform import TreeNode
from mnlg.xbar import XType


class Rule(typing.NamedTuple):
    x: XType
    head: str
    tree: TreeNode
