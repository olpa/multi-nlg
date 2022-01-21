from __future__ import annotations
import typing

from lxslt import TreeNode
from lojban_xbar import XType, XMax

CallableFunction = typing.Callable[[XMax], TreeNode]
CallableFunctionWithArgs = typing.List[typing.Union[
    # Function should be the first element, the rest
    # typing.Callable[[XMax, ...], TreeNode],  # python3.9+
    typing.Callable[..., TreeNode],  # python3.8
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
