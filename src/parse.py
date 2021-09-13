import io

import camxes_py


def to_s_expression(h, tree, print_space=True):
    if not isinstance(tree, list):
        if print_space:
            h.write(' ')
        h.write(tree)
        return
    h.write('(')
    to_s_expression(h, tree[0], print_space=False)
    for node in tree[1:]:
        to_s_expression(h, node)
    h.write(')')


class Wrapper:
    def __init__(self, tree):
        self.tree = tree

    def to_s_expression(self):
        h = io.StringIO()
        to_s_expression(h, self.tree)
        s = h.getvalue()
        return s


def parse(interlingua: str) -> Wrapper:
    return Wrapper(camxes_py.parse(interlingua))
