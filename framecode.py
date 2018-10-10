#!/usr/bin/python



import fileinput
import sys



# !!: skrypt nie lubi TAB w przetwarzanym tekscie

if __name__ == '__main__':

#    if   len(sys.argv) == 1:
#        FRAMECHAR = "/"
#    elif len(sys.argv) == 2:
#        FRAMECHAR = sys.argv[1]
#    else:
#        sys.stderr.write('Usage:')                                                ; sys.stderr.flush()
#        sys.stderr.write('  %s   [single_valid_comment_character]' % sys.argv[0]) ; sys.stderr.flush()
#        sys.stderr.write('\n')                                                    ; sys.stderr.flush()
#        sys.exit(1)
# JAKOS SIE TA SEKCJA GRYZIE Z fileinput

    FRAMECHAR = "/"

    ilines = []

    for line in fileinput.input():
        ilines.append(line.rstrip())


    ilenghts = [len(l) for l in ilines]
    imaxlen = max(ilenghts)

    desiredlen = imaxlen + 10

    head = []
    head.append(desiredlen*FRAMECHAR)
    head.append((desiredlen-2)*" "+2*FRAMECHAR)

    foot = []
    foot.append((desiredlen-2)*" "+2*FRAMECHAR)
    foot.append(desiredlen*FRAMECHAR)

    additions = []

    for l in ilenghts:
        additions.append((desiredlen-2-l)*" "+2*FRAMECHAR)


    for h in head:
        print h

    for l in zip(ilines, additions):
        print l[0] + l[1]

    for f in foot:
        print f
