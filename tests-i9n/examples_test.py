import unittest
from hamcrest import assert_that, equal_to

from mnlg.generate import MnlgInit, generate


def assert_example(mnlg: MnlgInit,
                   s_in: str,
                   expected_translations: dict[str, str]) -> None:
    ls_trans = generate(mnlg, interlingua=s_in)
    assert_that(ls_trans, equal_to(expected_translations))


class Example(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mnlg = MnlgInit('../gf/dist', 'Mnlg')

    def test_break_forzar(self):
        s_in = "la djan. pu gutnerkla le kumfa"
        expected_translations = {
                'de': 'Johann brach ins Zimmer ein.',
                'en': 'John broke into the room.',
                'es': 'Juan forzó la entrada al cuarto.',
                'ru': 'Иван ворвался в комнату.',
                'zh': '约翰闯进了房间。',
                }

        assert_example(self.mnlg, s_in, expected_translations)

    def test_stab_dar(self):
        s_in = "mi pu darxi la djan. le dakfu"
        expected_translations = {
                'de': 'Ich stach Johann.',
                'en': 'I stabbed John.',
                'es': 'Yo le di puñaladas a Juan.',
                'ru': 'Я ударил Ивана ножом.',
                'zh': '我刺伤了约翰。',
                }

        assert_example(self.mnlg, s_in, expected_translations)

    @staticmethod
    def xtest_san_francisco_sent1():
        s_in = "la sanfransiskos goi ko'a cu kulnu je" \
               "canja je jdini midju la nosenkalifornos"
        print(s_in)

    @staticmethod
    def xtest_san_francisco_sent2_adj():
        accidental = "la sandi'egos ce'o la sandi'egos ce'o la sanjoses lidne"
        determiner = f"ke ka {accidental} ke'e vomoi fi le nilxa'ugri"
        phrase = f"ko'a ke ka {determiner} ke'e tcadu la kalifornos"
        print(phrase)

    @staticmethod
    def xtest_san_francisco_sent2_poi():
        accidental = "la sandi'egos ce'o la sandi'egos ce'o la sanjoses lidne"
        determiner = f"vomoi ba zo'e noi {accidental} fi le nilxa'ugri"
        phrase = f"ko'a tcadu ba zo'e poi {determiner} la kalifornos"
        print(phrase)


if '__main__' == __name__:
    unittest.main()
