import typing
import unittest
from hamcrest import assert_that, equal_to

from mnlg.gf.stree_to_gf import stree_to_gf, stree_to_gf_fullstop
from mnlg.xbar import lexp_to_tree
from tests.util.fixture import load_stree, load_gf


n_max = ['N-MAX', ['N-BAR', ['N', 'word_N']]]
d_max = ['D-MAX', ['D-BAR', n_max]]
d_np = '(DetCN (DetQuant IndefArt NumSg) (UseN word_N))'


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
    def test_det():
        e = stree_to_gf(lexp_to_tree(d_max))

        assert_that(str(e), equal_to(
            'DetCN (DetQuant IndefArt NumSg) (UseN word_N)'))

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
    def test_verb_wrap_prep_complement():
        stree = lexp_to_tree(['V-MAX',
                              ['V-SPEC', d_max],
                              ['V-BAR', ['V', 'pred_V2'],
                               ['P-MAX', ['P-BAR', ['P', 'in_Prep'], d_max]]]])

        e = stree_to_gf(stree)

        p_np = f'(PrepNP in_Prep {d_np})'
        assert_that(str(e), equal_to(
            f'PredVP {d_np} (ComplSlash (SlashV2a pred_V2) '
            f'(CastAdvToNP {p_np}))'))

    @staticmethod
    def test_prep():
        stree = lexp_to_tree(['P-MAX',
                              ['P-BAR', ['P', 'in_Prep'], d_max]])

        e = stree_to_gf(stree)

        assert_that(str(e), equal_to(f'PrepNP in_Prep {d_np}'))


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

    def test_break_forzar(self):
        self.do_gf_test('break_forzar_en')

    def test_stab_dar_en(self):
        self.do_gf_test('stab_dar_en')


if '__main__' == __name__:
    unittest.main()
