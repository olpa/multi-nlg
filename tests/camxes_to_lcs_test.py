import unittest
from hamcrest import assert_that, equal_to
from util.fixture import load_camxes_parses, load_lcs

from mnlg.camxes_to_lcs import camxes_to_lcs


class CamxesToLcsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trees = load_camxes_parses()
        cls.lcs = load_lcs()

    def do_lcs_test(self, code_name):
        expected_lcs = self.lcs[code_name]
        source_camxes = self.trees[code_name]

        lcs = camxes_to_lcs(source_camxes)

        assert_that(lcs, equal_to(expected_lcs))

    def test_break_forzar(self):
        self.do_lcs_test('break_forzar')

    def test_stab_dar(self):
        self.do_lcs_test('stab_dar')


if '__main__' == __name__:
    unittest.main()
