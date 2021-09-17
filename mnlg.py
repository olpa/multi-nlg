import argparse
import os.path
import sys

from mnlg import MnlgInit, generate_one_sentence


def parse_command_line():
    parser = argparse.ArgumentParser(
        description='Read interlingua sentences from the '
                    'standard input and generate natural languages')
    parser.add_argument('--pgf',
                        dest='pgf',
                        help='path to the grammar file `Mnlg.pfg`',
                        required=True,
                        metavar='FILE')
    parser.add_argument('--lang',
                        dest='ls_lang',
                        required=True,
                        help='target languages separated by comma')
    return parser.parse_args()


def main():
    args = parse_command_line()

    languages = set(map(lambda s: s.strip(), args.ls_lang.split(',')))

    grammar_dir = os.path.dirname(args.pgf)
    grammar_name = os.path.splitext(os.path.basename(args.pgf))[0]
    mnlg_init = MnlgInit(grammar_dir, grammar_name)

    while True:
        print('>>> ', end='')
        sys.stdout.flush()
        lj = sys.stdin.readline()
        lj = lj.strip()
        print(f'lj: {lj}')

        for lang in languages:
            s = generate_one_sentence(mnlg_init, lj, lang)
            print(f'{lang}: {s}')


if '__main__' == __name__:
    main()
