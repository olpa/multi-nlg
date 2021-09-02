import unittest
from hamcrest import assert_that, equal_to

import generate


def assert_example(s_in, expected_translations):
    ls_trans = generate.generate(interlingua=s_in)
    assert_that(ls_trans, equal_to(expected_translations))


class Example(unittest.TestCase):

    @staticmethod
    def test_break_forzar():
        s_in = "la djan. pu gutnerkla le kumfa"
        expected_translations = {
                'de': 'Johann brach ins Zimmer ein.',
                'en': 'John broke into the room.',
                'es': 'Juan forzó la entrada al cuarto.',
                'ru': 'Джон ворвался в комнату.',
                'zh': '约翰闯进房间。',
                }

        assert_example(s_in, expected_translations)

    @staticmethod
    def test_stab_dar():
        s_in = "mi pu darxi la djan. le dakfu"
        expected_translations = {
                'de': 'Ich erstach Johann.',
                'en': 'I stabbed John.',
                'es': 'Yo le di puñaladas a Juan.',
                'ru': 'Я ударил Джона ножом.',
                'zh': '我刺伤了约翰。',
                }

        assert_example(s_in, expected_translations)


if '__main__' == __name__:
    unittest.main()
