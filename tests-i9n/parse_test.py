import unittest
from hamcrest import assert_that, equal_to
import sexpdata

import parse


def assert_example(s_in, expected_s_exp):
    expected_obj = sexpdata.loads(expected_s_exp)

    tree = parse.parse(interlingua=s_in)
    se_tree = tree.to_s_expression()

    se_obj_tree = sexpdata.loads(se_tree)
    assert_that(se_obj_tree, equal_to(expected_obj))


class ParseTest(unittest.TestCase):

    @staticmethod
    def test_break_forzar():
        s_in = "la djan. pu gutnerkla le kumfa"
        expected_s_exp = """
        (CAUSE Event
          (John Thing)
          (GO_Loc Event
            (John Thing)
            (TO_Loc ?
              (IN_Loc ?
                (John Thing)
                (ROOM Thing))))
          FORCEFULLY)
        """

        assert_example(s_in, expected_s_exp)

    @staticmethod
    def test_stab_dar():
        s_in = "mi pu darxi la djan. le dakfu"
        expected_s_exp = """
        (CAUSE Event
          (I Thing)
          (GO_Poss Event
            (KNIFE-WOUND Thing)
            (TOWARDS_Poss Path
              (AT_Poss Position
                (KNIFE-WOUND Thing)
                (John Thing)))))
        """

        assert_example(s_in, expected_s_exp)


if '__main__' == __name__:
    unittest.main()
