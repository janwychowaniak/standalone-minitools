#!/usr/bin/python




import sys
import os

import glob


COUNTER_STR_WIDTH = 5




def newname_gen(_n, _ext, _prefix):
    for counter in xrange(_n):
        counter_str = _prefix + '_' + '{0:0{width}}'.format(counter, width=COUNTER_STR_WIDTH) + '.' + _ext
        yield counter_str
        counter = counter + 1


def is_dict_safe_for_mv(_d):
    dict_keys = _d.keys()
    dict_vals = _d.values()
    for v in dict_vals:
        if v in dict_keys:
            return (False, v)
    return (True, None)


def quotes(_s):
    return '"' + _s + '"'


if __name__ == '__main__':

    ARGSNR = len(sys.argv)

    if ARGSNR != 3:
        print 'Usage:'
        print '  ' + sys.argv[0] + '   input_ext' + '   output_prefix'
        print
        sys.exit(1)


    INPUT_EXT = sys.argv[1]
    OUTPUT_PREFIX = sys.argv[2]


    # get unsorted list of concerned files

    extfiles = glob.glob('*.' +  INPUT_EXT)

    extfiles_sorted = sorted(extfiles)
    extfiles_sorted_r = sorted(extfiles, reverse=True)


    # get {name:newname} dicts

    extfiles_new = dict(zip(extfiles_sorted, newname_gen(len(extfiles_sorted), INPUT_EXT, OUTPUT_PREFIX)))
    extfiles_new_r = dict(zip(extfiles_sorted_r, newname_gen(len(extfiles_sorted_r), INPUT_EXT, OUTPUT_PREFIX)))

    extfiles_new_safety = is_dict_safe_for_mv(extfiles_new)    # == extfiles_new_r_safety check

    if not extfiles_new_safety[0]:
        sys.stderr.write("extfiles_new not safe." + os.linesep)
        sys.stderr.write("element: " + extfiles_new_safety[1] + os.linesep)
        sys.stderr.flush()
        sys.exit(2)


    # produce the "mv", finally

    print
    print '# rename forward'
    for k in sorted(extfiles_new.keys()):
        print 'mv -v', quotes(k), quotes(extfiles_new[k])

    print
    print '# rename reverse'
    for k in sorted(extfiles_new_r.keys()):
        print 'mv -v', quotes(k), quotes(extfiles_new_r[k])

    print

