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
        s_in = 'la djan. pu gutnerkla le kumfa'
        expected_translations = {
                'de': 'Johann brach ins Zimmer ein.',
                'en': 'John broke into the room.',
                'es': 'Juan forzó la entrada al cuarto.',
                'ru': 'Иван ворвался в комнату.',
                'zh': '约翰闯进了房间。',
                }

        assert_example(self.mnlg, s_in, expected_translations)

    def test_stab_dar(self):
        s_in = 'mi pu darxi la djan. le dakfu'
        expected_translations = {
                'de': 'Ich stach Johann.',
                'en': 'I stabbed John.',
                'es': 'Yo le di puñaladas a Juan.',
                'ru': 'Я ударил Ивана ножом.',
                'zh': '我刺伤了约翰。',
                }

        assert_example(self.mnlg, s_in, expected_translations)

    def test_san_francisco_sent1(self):
        s_in = "la sanfransiskos goi ko'a cu kulnu je " \
               'canja je jdini midju la nosenkalifornos'
        expected_translations = {
            'de': 'San Francisco ist das kulturelle, kommerzielle und '
                  'finanzielle Zentrum Nordkaliforniens.',
            'en': 'San Francisco is the cultural, commercial and financial '
                  'center of Northern California.',
            'es': 'San Francisco es el centro cultural, comercial y '
                  'financiero del Norte de California.',
            'ru': 'Сан-Франциско является культурным, коммерческим и '
                  'финансовым центром Северной Калифорнии.',
            'zh': '旧金山是北加州的文化、商业和金融中心。',
        }

        assert_example(self.mnlg, s_in, expected_translations)

    def xtest_san_francisco_sent2(self):
        accidental = "la losangeles ce'o la sandi'egos ce'o la sanjoses lidne"
        determiner = f"ke ka {accidental} ke'e vomoi fi le xa'ugri"
        s_in = f"ko'a ke ka {determiner} ke'e tcadu la kalifornos"
        expected_translations = {
            'de': 'Es ist die viertgrößte Stadt in Kalifornien, nach Los '
                  'Angeles, San Diego und San Jose.',
            'en': 'It is fourth city of California by population, after '
                  'Los Angeles, San Diego and San Jose.',
            'es': 'Es la cuarta ciudad de California por población, después '
                  'de Los Ángeles, San Diego y San José.',
            'ru': 'Это четвертый по численности населения город в Калифорнии '
                  'после Лос-Анджелеса, Сан-Диего и Сан-Хосе.',
            'zh': '它是加利福尼亚州人口第四大的城市， 仅次于洛杉矶，圣地亚哥和圣何塞。',
        }
        assert_example(self.mnlg, s_in, expected_translations)

    def xtest_marie_curie(self):
        s_in = ''
        expected_translations = {
            'de': '',
            'en': 'Marie Curie was the only person to receive the Nobel '
                  'Prize in two different scientific categories.',
            'es': '',
            'ru': '',
            'zh': '',
        }
        assert_example(self.mnlg, s_in, expected_translations)


if '__main__' == __name__:
    unittest.main()
