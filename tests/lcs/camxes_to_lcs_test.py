import unittest
from hamcrest import assert_that, equal_to
from tests.util.fixture import load_camxes_parses, load_lcs

from mnlg.lcs.camxes_to_lcs import camxes_to_lcs, SumtiAllocator


def wrap_i_max(v_max):
    return ['I-MAX', ['I-BAR', ['I'], v_max]]


def wrap_i_v_max(v, *compl):
    if isinstance(v, str):
        v = ['V', v]
    return wrap_i_max(['V-MAX', ['V-FRAME', v, *compl]])


def wrap_n_max(name):
    return ['N-MAX', ['N-BAR', ['N', name]]]


class CamxesToLcsTest(unittest.TestCase):
    trees = load_camxes_parses()

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

    @staticmethod
    def test_tense_tag():
        # 'pu prami', only 'pu' is interesting in the test
        tree = CamxesToLcsTest.trees['pu_prami']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            ['I-MAX', ['I-BAR', ['I', ['tag', 'pu']],
                       ['V-MAX', ['V-FRAME', ['V', 'prami']]]]]))

    @staticmethod
    def test_selbri_alone():
        tree = CamxesToLcsTest.trees['prami']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(wrap_i_v_max('prami')))

    @staticmethod
    def test_selbri_adjunct():
        tree = CamxesToLcsTest.trees['barda_prami']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_max(['V-MAX',
                        ['V-BAR',
                         ['V-FRAME', ['V', 'prami']],
                         ['V-MAX', ['V-FRAME', ['V', 'barda']]]]])))

    @staticmethod
    def test_selbri_moi():
        tree = CamxesToLcsTest.trees['vomoi']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            ['I-MAX', ['I-BAR', ['I'],
                       ['V-MAX', ['V-FRAME',
                                  ['V', ['tag', 'moi'], 'vo']]]]]))

    @staticmethod
    def test_nu_clause():
        tree = CamxesToLcsTest.trees['nu_prami_kei_klama']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_max(
                ['V-MAX',
                 ['V-BAR',
                  ['V-FRAME', ['V', 'klama']],
                  ['I-MAX', ['I-BAR', ['I'],
                             ['V-MAX',
                              ['V-FRAME', ['V', 'prami']]]]]]])))

    @staticmethod
    def test_joi():
        tree = CamxesToLcsTest.trees['mi_cehe_do_ceho_maha_klama']

        lcs = camxes_to_lcs(tree)

        j_maha = ['J-MAX', ['J-BAR',
                            ['J', "ce'o"],
                            ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'],
                                                 "ma'a"]]]]]
        j_do = ['J-MAX', ['J-BAR',
                          ['J', "ce'o"],
                          ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'],
                                               'do']]]]]
        assert_that(lcs, equal_to(
            wrap_i_v_max(
                'klama',
                ['J-MAX', ['J-BAR',
                           ['J-BAR',
                            ['J-BAR',
                             ['J', ''],
                             ['N-MAX', ['N-BAR',
                                        ['N', ['tag', 'pron'], 'mi']]]],
                            j_do],
                           j_maha]])))

    @staticmethod
    def test_poi():
        tree = CamxesToLcsTest.trees['lo_prami_poi_barda_kuho_klama']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_v_max(
                'klama',
                ['D-MAX', ['D-BAR',
                           ['D', ['tag', 'lo']],
                           ['N-MAX',
                            ['N-BAR',
                             ['N-BAR', ['N', 'prami']],
                             ['C-MAX', ['C-BAR', ['C', 'poi'],
                                        wrap_i_v_max('barda')]]
                             ]]]])))

    @staticmethod
    def test_ja():
        tree = CamxesToLcsTest.trees['kulnu_je_canja_je_jdini_midju']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_max(
                ['V-MAX',
                 ['V-BAR',
                  ['V-FRAME', ['V', 'midju']],
                  ['J-MAX',
                   ['J-BAR',
                    ['J-BAR',
                     ['J-BAR',
                      ['J', ''],
                      wrap_n_max('kulnu')],
                     ['J-MAX', ['J-BAR', ['J', 'je'], wrap_n_max('canja')]]],
                    ['J-MAX', ['J-BAR', ['J', 'je'], wrap_n_max('jdini')]]
                    ]]]])))

    @staticmethod
    def test_fa():
        tree = CamxesToLcsTest.trees['fi_mi_klama_fa_do']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_v_max(
                'klama',
                ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'do']]],
                ['N-MAX', ['N-BAR', ['N', ['tag', 'zo\'e'], '']]],
                ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'mi']]]
            )))

    @staticmethod
    def test_be_bei():
        tree = CamxesToLcsTest.trees['barda_be_mi_bei_fi_do_klama']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_max(
                ['V-MAX',
                 ['V-BAR',
                  ['V-FRAME', ['V', 'klama']],
                  ['V-MAX',
                   ['V-FRAME',
                    ['V', 'barda'],
                    ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'mi']]],
                    ['N-MAX', ['N-BAR', ['N', ['tag', 'zo\'e'], '']]],
                    ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'do']]]
                    ]]]]
            )))

    @staticmethod
    def test_mix_bei_poi():
        tree = CamxesToLcsTest.trees['sutra_be_zohe_poi_barda_beho_klama']

        lcs = camxes_to_lcs(tree)

        assert_that(lcs, equal_to(
            wrap_i_max(
                ['V-MAX',
                 ['V-BAR',
                  ['V-FRAME', ['V', 'klama']],
                  ['V-MAX',
                   ['V-FRAME',
                    ['V', 'sutra'],
                    ['N-MAX',
                     ['N-BAR',
                      ['N-BAR', ['N', ['tag', 'pron'], 'zo\'e']],
                      ['C-MAX', ['C-BAR', ['C', 'poi'], wrap_i_v_max('barda')]]
                      ]
                     ]
                    ]]
                  ]]
            )))


class SumtiAllocatorTest(unittest.TestCase):
    n1 = ['N-MAX', ['N-BAR', ['N', 'n1_N']]]
    n2 = ['N-MAX', ['N-BAR', ['N', 'n2_N']]]
    n3 = ['N-MAX', ['N-BAR', ['N', 'n3_N']]]
    zohe = ['N-MAX', ['N-BAR', ['N', ['tag', 'zo\'e'], '']]]

    def test_fill_in_order(self):
        sa = SumtiAllocator()

        sa.push(self.n1)
        sa.push(self.n2)
        sa.push(self.n3)

        assert_that(sa.get_sumti(), equal_to([self.n1, self.n2, self.n3]))

    def test_start_from_x2_after_selbri(self):
        sa = SumtiAllocator()

        sa.push_selbri()
        sa.push(self.n1)
        sa.push(self.n2)

        assert_that(sa.get_sumti(), equal_to([self.zohe, self.n1, self.n2]))

    def test_start_from_what_was_before_selbri(self):
        sa = SumtiAllocator()

        sa.push(['FA_clause', 'fi'])
        sa.push(self.n1)
        sa.push_selbri()
        sa.push(self.n2)

        assert_that(sa.get_sumti(),
                    equal_to([self.zohe, self.zohe, self.n1, self.n2]))

    def test_start_find_next_free_position(self):
        sa = SumtiAllocator()

        sa.push(['FA_clause', 'fe'])
        sa.push(self.n1)
        sa.push(['FA_clause', 'fa'])
        sa.push(self.n2)
        sa.push(self.n3)  # after 'fa', 'fe' is already taken

        assert_that(sa.get_sumti(), equal_to([self.n2, self.n1, self.n3]))


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
