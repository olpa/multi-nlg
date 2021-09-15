import typing
from enum import Enum


class XType(Enum):
    I = 1  # noqa: E741
    N = 2
    V = 3
    A = 4

    def __str__(self):
        return self.name


class XHead:
    def __init__(self,
                 type_: XType,
                 s: typing.Union[str, None],
                 tags: list[str] = ()):
        self.type = type_
        self.s = s
        self.tags = list(tags)

    def __str__(self):
        ls = [self.s if self.s is not None else 'None', *self.tags]
        return f'{self.type}-HEAD<{", ".join(ls)}>'


class XBarBase:
    def __init__(self,
                 head: XHead,
                 compl: typing.Union['XMax', None] = None,
                 ):
        self.type = head.type
        self.head = head
        self.compl = compl

    def __str__(self) -> str:
        return f'{self.type}-BAR<{self.head}{",..." if self.compl else ""}>'


class XBarFrame:
    def __init__(self,
                 head: XHead,
                 *compl: list['XMax']
                 ):
        self.type = head.type
        self.head = head
        self.compl = compl

    def __str__(self) -> str:
        return f'{self.type}-BAR<{self.head},...>'


class XBarRec:
    def __init__(self, bar: 'XBar', adj: 'XMax'):
        self.bar = bar
        self.adj = adj


XBar = typing.Union[XBarBase, XBarFrame, XBarRec]


def isinstance_xbar(o: object) -> bool:
    return isinstance(o, XBarBase) or \
           isinstance(o, XBarFrame) or isinstance(o, XBarRec)


class XSpecTag:
    def __init__(self, tags: list[str]):
        self.tags = list(tags)

    def __str__(self):
        return f'XSpecTag<{",".join(self.tags)}>'


XSpec = typing.Union[XSpecTag, 'XMax']


def isinstance_xspec(o: object) -> bool:
    return isinstance(o, XSpecTag) or isinstance(o, XMax)


class XMax:
    def __init__(self, spec: typing.Union['XMax', XSpec, None], xbar: XBar):
        self.spec = spec
        self.xbar = xbar
        self.type = xbar.type

    def __str__(self):
        head = self.to_head()
        s = head.s if head else ''
        return f'{self.type}-MAX<{s}>'

    def to_head(self) -> typing.Optional[XHead]:
        bar = self.to_bar()
        return bar and bar.head

    def to_complement(self) -> typing.Union[list['XMax'], 'XMax', None]:
        bar = self.to_bar()
        return bar and bar.compl

    def to_spec(self):
        return self.spec

    def to_bar(self) -> typing.Union[XBarBase, XBarFrame, None]:
        bar = self.xbar
        while isinstance(bar, XBarRec):
            bar = bar.bar
        return bar
