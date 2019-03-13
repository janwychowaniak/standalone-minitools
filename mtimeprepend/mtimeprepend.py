#!/usr/bin/python


import datetime as dt

from os import listdir, stat
from os.path import isfile, join



def get_modtime(filename):
    '''
    Gets the file modification time as an epoch timestamp (e.g. '1546702438')
    '''
    statbuf = stat(filename)
    return int(statbuf.st_mtime)


def epoch_to_yyyymmdd(_timestamp):
    return dt.datetime.utcfromtimestamp(_timestamp).strftime("%Y%m%d")


def prepend(_name, _toprep):
    return _toprep + '-' + _name


def update_dict(_file_modtime_dict):

    updated_d = {}

    for row in _file_modtime_dict:
        val = prepend(row, _file_modtime_dict[row])
        updated_d.update({row : val})

    return updated_d



def main():

    # get list of files only

    mypath = '.'

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



    # get {file:modtime} dict

    file_modtime_dict = {}

    for item in onlyfiles:
        file_modtime_dict[item] = epoch_to_yyyymmdd(get_modtime(item))



    # print

    print

    prepended_dict = update_dict(file_modtime_dict)

    for i in prepended_dict:
        print 'mv', i, prepended_dict[i], ';'

    print


if __name__ == '__main__':
    main()
