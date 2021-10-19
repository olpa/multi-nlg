import typing

from mnlg.transform import TreeNode
from mnlg.xbar import XType, XMax

CallableFunction = typing.Callable[[XMax], TreeNode]
CallableFunctionWithArgs = list[typing.Union[
    # Function should be the first element, the rest
    typing.Callable[[XMax, ...], TreeNode],
    # The rest is arguments
    str
]]


class Rule(typing.NamedTuple):
    x: XType
    head: typing.Optional[str]
    tree: TreeNode
    vars: typing.Optional[
        dict[str, typing.Union[str,
                               CallableFunction,
                               CallableFunctionWithArgs]]]
    adj: list[TreeNode]


class LcsToDtreeContext(typing.NamedTuple):
    rules: list[Rule]
    lcs_to_dtree: typing.Callable[
        [list[Rule], XMax, typing.Optional[XType]], TreeNode]
