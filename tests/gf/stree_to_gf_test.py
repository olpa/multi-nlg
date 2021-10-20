import typing
import unittest
from hamcrest import assert_that, equal_to

from mnlg.gf.stree_to_gf import stree_to_gf, stree_to_gf_fullstop
from mnlg.xbar import lexp_to_tree, XMax
from tests.util.fixture import load_stree, load_gf
from mnlg.transform import TreeNode


n_max = ['N-MAX', ['N-BAR', ['N', 'word_N']]]
d_max = ['D-MAX', ['D-BAR', ['D'], n_max]]
d_np = '(DetCN (DetQuant IndefArt NumSg) (UseN word_N))'


def mk_d_max(word: str) -> TreeNode:
    return ['D-MAX', ['D-BAR', ['D'], ['N-MAX', ['N-BAR', ['N', word]]]]]


def str_d_max(word: str) -> str:
    return f'(DetCN (DetQuant IndefArt NumSg) (UseN {word}))'


class StreeToGfTest(unittest.TestCase):

    @staticmethod
    def test_noun():
        stree = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'room_N']]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to('UseN room_N'))

    @staticmethod
    def test_noun_that_is_personal_name():
        stree = lexp_to_tree(['N-MAX',
                              ['N-BAR', ['N', 'name_PN', ['tag', 'pn']]]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to('UsePN name_PN'))

    @staticmethod
    def test_noun_that_is_pronoun():
        stree = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'i_Pron']]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to('UsePron i_Pron'))

    @staticmethod
    def test_noun_that_is_already_common():
        stree = lexp_to_tree(['N-MAX', ['N-BAR', ['N', 'some_CN']]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to('some_CN'))

    @staticmethod
    def test_det():
        e = stree_to_gf(lexp_to_tree(d_max))

        assert_that(str(e), equal_to(
            'DetCN (DetQuant IndefArt NumSg) (UseN word_N)'))

    @staticmethod
    def test_det_loi():
        e = stree_to_gf(lexp_to_tree(
            ['D-MAX', ['D-BAR', ['D', ['tag', 'mass']], n_max]]))

        assert_that(str(e), equal_to(
            'MassLoi (UseN word_N)'))

    @staticmethod
    def test_infl():
        stree = lexp_to_tree(
            ['I-MAX', ['I-BAR', ['I',
                                 ['tag', 'Tense', 'TPast'],
                                 ['tag', 'Ant', 'AAnter']]]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to('UseCl (TTAnt TPast AAnter) PPos'))

    @staticmethod
    def test_verb_without_complement():
        stree = lexp_to_tree(
            ['V-MAX', ['V-SPEC', d_max], ['V-BAR', ['V', 'pred_V']]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(f'PredVP {d_np} (UseV pred_V)'))

    @staticmethod
    def test_verb_with_complement():
        stree = lexp_to_tree(['V-MAX',
                              ['V-SPEC', d_max],
                              ['V-BAR', ['V', 'pred_V2'], d_max]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(
            f'PredVP {d_np} (ComplSlash (SlashV2a pred_V2) {d_np})'))

    @staticmethod
    def test_verb_with_pp_adjunct():
        stree = lexp_to_tree(
            ['V-MAX',
             ['V-SPEC', d_max],
             ['V-BAR',
              ['V-BAR', ['V', 'some_V']],
              ['P-MAX', ['P-BAR', ['P', 'some_P'], d_max
                         ]]]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(
            f'PredVP {d_np} (AdvVP (UseV some_V) (PrepNP some_P {d_np}))'))

    @staticmethod
    def test_prep():
        stree = lexp_to_tree(['P-MAX',
                              ['P-BAR', ['P', 'in_Prep'], d_max]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(f'PrepNP in_Prep {d_np}'))

    @staticmethod
    def mk_lexp_vp_shell(inner_spec: TreeNode) -> XMax:
        lexp_to_tree(mk_d_max('theme_N'))
        lexp_to_tree(['V-MAX',
                      ['V-SPEC', inner_spec],
                      ['V-BAR',
                       ['V', None, ['tag', 'trace']],
                       mk_d_max('theme_N')]])
        # subject_N gives theme_N to recipient_N
        return lexp_to_tree(
            ['V-MAX', ['V-SPEC', mk_d_max('subject_N')],
             ['V-BAR', ['V', 'give_V3'],
              ['V-MAX',
               ['V-SPEC', inner_spec],
               ['V-BAR',
                ['V', None, ['tag', 'trace']],
                mk_d_max('theme_N')]]]])

    @staticmethod
    def mk_s_vp_shell(s_command: str, s_inner: str) -> str:
        return (f'PredVP {str_d_max("subject_N")} ({s_command} '
                f'(CastV3toV give_V3) {s_inner} {str_d_max("theme_N")})')

    @staticmethod
    def test_vp_shell():
        stree = StreeToGfTest.mk_lexp_vp_shell(mk_d_max('recipient_N'))
        expected_gf = StreeToGfTest.mk_s_vp_shell(
            'VPshell', str_d_max('recipient_N'))

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_vp_shell_direct():
        recipient = ['N-MAX', ['N-BAR', ['N', ['tag', 'pron'], 'i_Pron']]]
        stree = StreeToGfTest.mk_lexp_vp_shell(recipient)
        expected_gf = StreeToGfTest.mk_s_vp_shell(
            'VPshellDirect', '(UsePron i_Pron)')

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_indirect_clitic():
        clitic_tag = ['tag', 'clitic', 'indirect']
        lexp = ['V-MAX',
                ['V-SPEC', d_max],
                ['V-BAR',
                 ['V-BAR', ['V', 'do_V']],
                 ['N-MAX', ['N-BAR', ['N', 'john_PN', clitic_tag]]]]]
        expected_gf = f'PredVP {d_np} (WithIndirectClitic ' + \
                      '(UsePN john_PN) (UseV do_V))'

        e = stree_to_gf(lexp_to_tree(lexp))

        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_adjective_and():
        kulnu = ["J-BAR", ["J", ""], ["A-MAX", ["A-BAR", ["A", "kulnu_A"]]]]
        canja = ["J-MAX", ["J-BAR", ["J", "je"],
                           ["A-MAX", ["A-BAR", ["A", "canja_A"]]]]]
        jdini = ["J-MAX", ["J-BAR", ["J", "je"],
                           ["A-MAX", ["A-BAR", ["A", "jdini_A"]]]]]
        lexp = ["J-MAX", ["J-BAR", ["J-BAR", kulnu, canja], jdini]]
        expected_gf = 'ConjAP and_Conj (ConsAP (BaseAP (PositA kulnu_A) ' \
                      '(PositA canja_A)) (PositA jdini_A))'

        e = stree_to_gf(lexp_to_tree(lexp))

        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_noun_with_adjective():
        lexp = ["N-MAX", ["N-BAR",
                          ["N-BAR", ["N", "city_N"]],
                          ["A-MAX", ["A-BAR", ["A", "nice_A"]]]]]

        e = stree_to_gf(lexp_to_tree(lexp))

        expected_gf = 'AdjCN (PositA nice_A) (UseN city_N)'
        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_noun_with_and():
        kulnu = ["J-BAR", ["J", ""], ["A-MAX", ["A-BAR", ["A", "kulnu_A"]]]]
        canja = ["J-MAX", ["J-BAR", ["J", "je"],
                           ["A-MAX", ["A-BAR", ["A", "canja_A"]]]]]
        lexp = ["N-MAX", ["N-BAR",
                          ["N-BAR", ["N", "city_N"]],
                          ["J-MAX", ["J-BAR", kulnu, canja]]]]

        e = stree_to_gf(lexp_to_tree(lexp))

        expected_gf = 'AdjCN (ConjAP and_Conj (BaseAP (PositA kulnu_A) ' \
                      '(PositA canja_A))) (UseN city_N)'
        assert_that(str(e), equal_to(expected_gf))

    @staticmethod
    def test_noun_with_adjunct_recursive():
        lexp = ["N-MAX", ["N-BAR",
                          ["N-BAR",
                           ["N-BAR", ["N", "thing_N"]],
                           ["A-MAX", ["A-BAR", ["A", "blue_A"]]]],
                          ["A-MAX", ["A-BAR", ["A", "red_A"]]]]]

        e = stree_to_gf(lexp_to_tree(lexp))

        expected_gf = 'AdjCN (PositA red_A) ' \
                      '(AdjCN (PositA blue_A) (UseN thing_N))'
        assert_that(str(e), equal_to(expected_gf))


class StreeToGfExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stree = load_stree()
        cls.gf = load_gf()

    def do_gf_test(self, code_name):
        source_stree = lexp_to_tree(typing.cast(list, self.stree[code_name]))
        expected_gf = self.gf[code_name]

        gf = stree_to_gf_fullstop(source_stree)

        assert_that(str(gf), equal_to(expected_gf))

    def test_break_forzar_en(self):
        self.do_gf_test('break_forzar_en')

    def test_stab_dar_en(self):
        self.do_gf_test('stab_dar_en')

    def test_break_forzar_es(self):
        self.do_gf_test('break_forzar_es')

    def test_stab_dar_es(self):
        self.do_gf_test('stab_dar_es')

    def test_break_forzar_de(self):
        self.do_gf_test('break_forzar_de')

    def test_stab_dar_de(self):
        self.do_gf_test('stab_dar_de')

    def test_break_forzar_ru(self):
        self.do_gf_test('break_forzar_ru')

    def test_stab_dar_ru(self):
        self.do_gf_test('stab_dar_ru')

    def test_break_forzar_zh(self):
        self.do_gf_test('break_forzar_zh')

    def test_stab_dar_zh(self):
        self.do_gf_test('stab_dar_zh')


if '__main__' == __name__:
    unittest.main()
