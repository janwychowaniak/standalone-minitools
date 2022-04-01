#!/usr/bin/python3


import sys
from random import randint



def random_digit():
    return randint(0, 9)


def transform_digit(char_: str):
    return str(random_digit()) if char_.isdigit() else char_


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('*** Usage:', file=sys.stderr)
        print(f'    {sys.argv[0]}   in_file', file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)

    FILENAME = sys.argv[1]

    #
    with open(FILENAME) as file:
        single_str = file.read()

    print(''.join([transform_digit(c) for c in single_str]))
