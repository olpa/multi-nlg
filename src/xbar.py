import typing
from enum import Enum


class XType(Enum):
    I = 1  # noqa: E741
    N = 2
    V = 3
    A = 4


class XHeadMarker(Enum):
    PU = 1


XHead = typing.Union[str, XHeadMarker]


class XBarBase:
    def __init__(self,
                 type_: XType,
                 head: XHead,
                 compl: typing.Union['XMax', None] = None,
                 adj: typing.Union['XMax', None] = None
                 ):
        self.type = type_
        self.head = head
        self.compl = compl
        self.adj = adj


class XBarFrame:
    def __init__(self,
                 head: XHead,
                 compl: typing.Union[list['XMax'], None],
                 adj: typing.Union['XMax', None] = None
                 ):
        self.type = XType.V
        self.head = head
        self.compl = compl
        self.adj = adj


class XBarRec:
    def __init__(self, child: 'XBar', adj: 'XMax'):
        self.child = child
        self.adj = adj


XBar = typing.Union[XBarBase, XBarFrame, XBarRec]


class XSpec(Enum):
    LA = 1
    LE = 2


class XMax:
    def __init__(self, spec: typing.Union['XMax', XSpec, None], xbar: XBar):
        self.spec = spec
        self.xbar = xbar
