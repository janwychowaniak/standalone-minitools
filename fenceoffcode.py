#!/usr/bin/python

# !!: skrypt nie lubi TAB w przetwarzanym tekscie

import sys

FRAMECHAR = "#"

if __name__ == '__main__':

    if len(sys.argv) == 1:
        LABEL = ''
    elif len(sys.argv) == 2:
        LABEL = sys.argv[1]
    else:
        raise Exception("Should get one argument (for label)")

    ilines = sys.stdin.readlines()

    imaxlen = max([len(l) for l in ilines])

    desiredlen = imaxlen + 3

    head = []
    if LABEL:
        head.append(f'{FRAMECHAR} {LABEL} {FRAMECHAR*(desiredlen-len(LABEL)-3)}')
    else:
        head.append(desiredlen*FRAMECHAR)
    head.append(FRAMECHAR)

    foot = []
    foot.append(FRAMECHAR)
    foot.append(desiredlen*FRAMECHAR)

    print()
    print('-'*imaxlen*2)
    print()

    for h in head:
        print(h)

    for l in ilines:
        print(l.rstrip())

    for f in foot:
        print(f)

    print()
