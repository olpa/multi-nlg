import unittest
from hamcrest import assert_that, equal_to
from util.fixture import load_camxes_parses, load_lcs

from mnlg.camxes_to_lcs import camxes_to_lcs


class CamxesToLcsTest(unittest.TestCase):

    @staticmethod
    def test_personal_name():
        tree = ['sumti_6', ['LA_clause', [['LA', 'la']]],
                [['CMEVLA_clause', [['CMEVLA', ['cmevla', 'djan']]]]]]

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            ['N-MAX', ['N-BAR', ['N', ['tag', 'pn'], 'djan']]]))

    @staticmethod
    def test_pronoun():
        tree = ["sumti_6", ["KOhA_clause", [["KOhA", "mi"]]]]

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'mi']]]))

    @staticmethod
    def test_le():
        tree = ["sumti_6", ["LE_clause", [["LE", "le"]]], ["sumti_tail",
                ["sumti_tail_1", ["selbri", ["selbri_1", ["selbri_2",
                 ["selbri_3", ["selbri_4", ["selbri_5", ["selbri_6",
                  ["tanru_unit", ["tanru_unit_1", ["tanru_unit_2",
                   ["BRIVLA_clause", [["BRIVLA",
                    ["gismu", "kumfa"]]]]]]]]]]]]]]]], ["KU"]]

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            ['D-MAX', ['D-BAR', ['D', ['tag', 'le']],
                       ['N-MAX', ['N-BAR', ['N', 'kumfa']]]]]))


class CamxesToLcsExamplesTest(unittest.TestCase):
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
