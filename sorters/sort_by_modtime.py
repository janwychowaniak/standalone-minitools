#!/usr/bin/python




import sys
import os
import time
from os import listdir
from os.path import isfile, join




USAGEMSG = \
'''
{}  FILES_PREFIX  [OFFSET]

    The script offers the possibility to perform batch rename of the files present
    at the current location, with the aim of reflecting their chronological order
    (based on the modification times) in their name scheme. The core of the new name
    is based on the FILES_PREFIX, the second part of the new name is a number
    indicating their chronological order. An additional parameter is available if
    the numbering is not supposed to start from 0.

'''




ERRMSG = \
'''
 *** file_modtime_dict.values() not unique. That's bad.
     If you wish to manually fix it, here is how (e.g.):
         touch -t 201504042045.26 SAM_4998.JPG         // [[CC]YY]MMDDhhmm[.ss]
'''



def get_modtime(filename):
    statbuf = os.stat(filename)
    return int(statbuf.st_mtime)


def unique_values(g):
    '''
    Does the g collection have unique values?
    '''
    s = set()
    for x in g:
        if x in s:
            print x, '\t(', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)), ')'
            return False
        s.add(x)
    return True


def sort_dict_by_val(x):
    '''
    "sort" a dict.
    [http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value]
    '''
    import operator
    return sorted(x.iteritems(), key=operator.itemgetter(1))




if __name__ == '__main__':

    ARGSNR = len(sys.argv)

    if ARGSNR != 2 and ARGSNR != 3:
        sys.stderr.write(USAGEMSG.format(sys.argv[0]))
        sys.exit(1)


    COUNTER_STR_WIDTH = 4

    PREFIX = sys.argv[1]

    OFFSET = 0 if ARGSNR == 2 else int(sys.argv[2])
    
    # get list of files only
    mypath = '.'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

    # get {file:modtime} dict
    file_modtime_dict = {}
    for p in onlyfiles:
        file_modtime_dict[p] = get_modtime(p)

    # are modtimes unique? if not, terminate
    if not unique_values(file_modtime_dict.values()):
        sys.stderr.write(ERRMSG)
        sys.exit(2)
        
    # sorting filenames: modtime-sorted {file:modtime} "dict" (list'o'tuples)
    modtime_sorted_dict      = sort_dict_by_val(file_modtime_dict)
    modtime_sorted_dict_keys = [entry[0] for entry in modtime_sorted_dict]    # ".keys()"

    # get {file:lower(ext)} dict
    file_ext_dict = {}
    for p in modtime_sorted_dict_keys:
        file_ext_dict[p] = os.path.splitext(p)[1].lower()
    
    # get {old filename : new filename } "dict" (list'o'lists)
    ofile_nfile_dict = []
    for p in modtime_sorted_dict_keys:
        counter     = len(ofile_nfile_dict)+1 + OFFSET
        counter_str = '{0:0{width}}'.format(counter, width=COUNTER_STR_WIDTH)
        ofile_nfile_dict.append([p, ''.join( [PREFIX, '_', counter_str, file_ext_dict[p]] )])


    # produce the "mv", finally
    for p in ofile_nfile_dict:
        print 'mv -v', p[0], p[1]

