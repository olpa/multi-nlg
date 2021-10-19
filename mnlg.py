import argparse
import os.path
import sys
import json
from json import JSONDecodeError

from mnlg import MnlgInit, generate_one_sentence, Step


def parse_command_line():
    ls_steps = list(map(str, Step.__members__))
    s_steps = ','.join(ls_steps)
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
    parser.add_argument('--begin',
                        dest='begin',
                        help=f'begin with output data of a step: {s_steps}',
                        choices=ls_steps)
    parser.add_argument('--end',
                        dest='end',
                        help=f'end at a step: {s_steps}',
                        choices=ls_steps)
    return parser.parse_args()


def main():
    args = parse_command_line()

    languages = set(map(lambda s: s.strip(), args.ls_lang.split(',')))

    grammar_dir = os.path.dirname(args.pgf)
    grammar_name = os.path.splitext(os.path.basename(args.pgf))[0]
    mnlg_init = MnlgInit(grammar_dir, grammar_name)

    need_step = Step[args.begin] if args.begin else Step.lojban
    begin_step = need_step + 1
    end_step = Step[args.end] if args.end else Step.natural

    if sys.stdin.isatty():
        import readline  # noqa: F401

    while True:
        sys.stdout.flush()
        if sys.stdin.isatty():
            try:
                so_far = input(f'{need_step.name}>>> ')
            except EOFError:
                break
        else:
            so_far = sys.stdin.readline()
        if not so_far:
            if sys.stdin.isatty():
                print()
            break
        so_far = so_far.strip()
        if not so_far:
            continue

        if so_far[0] == '[':
            try:
                so_far = json.loads(so_far)
            except JSONDecodeError:
                print('Bad JSON', file=sys.stderr)
                continue

        so_far = generate_one_sentence(
            mnlg_init, so_far, 'none', begin_step, min(end_step, Step.lcs)
        )

        if end_step <= Step.lcs:
            s = so_far if isinstance(so_far, str) else json.dumps(so_far)
            print(f'{end_step.name}: {s}')
        else:
            for lang in languages:
                s = generate_one_sentence(
                    mnlg_init,
                    so_far,
                    lang,
                    max(begin_step, Step.dtree),
                    end_step
                )
                if not isinstance(s, str):
                    if isinstance(s, list):
                        s = json.dumps(s)
                    else:
                        s = str(s)
                print(f'{lang}: {s}')


if '__main__' == __name__:
    main()
