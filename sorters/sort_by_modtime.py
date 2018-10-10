#!/usr/bin/python




import sys
import os
import time
from os import listdir
from os.path import isfile, join





def get_modtime(filename):
	statbuf = os.stat(filename)
	return int(statbuf.st_mtime)


# does the g collection have unique values?
def unique_values(g):
	s = set()
	for x in g:
		if x in s:
			print x, '\t(', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)), ')'
			return False
		s.add(x)
	return True


# "sort" a dict. http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
def sort_dict_by_val(x):
	import operator
	return sorted(x.iteritems(), key=operator.itemgetter(1))




# ////////////////////////////////////////////////////////////////////////
# for py.test
# ------------------

def test_unique_values():

	file_modtime_dict_unique = {}
	file_modtime_dict_nonunique = {}

	file_modtime_dict_unique['AUD0056.3gp'] = 1388141568
	file_modtime_dict_unique['AUD0057.3gp'] = 1388144212
	file_modtime_dict_unique['AUD0058.3gp'] = 1388146678

	file_modtime_dict_nonunique['AUD0056.3gp'] = 1388141568
	file_modtime_dict_nonunique['AUD0057.3gp'] = 1388144212	# <--
	file_modtime_dict_nonunique['AUD0058.3gp'] = 1388144212	# <--
	file_modtime_dict_nonunique['AUD0059.3gp'] = 1388146678

	assert unique_values(file_modtime_dict_unique.values())    == True
	assert unique_values(file_modtime_dict_nonunique.values()) == False

# ------------------

def test_sort_dict_by_val():

	x_orig      = {"1":2, "3":4, "4":3, "2":1, "0":0}
	x_valsorted = [("0",0), ("2",1), ("1",2), ("4",3), ("3",4)]

	assert sort_dict_by_val (x_orig) == x_valsorted

# ////////////////////////////////////////////////////////////////////////




if __name__ == '__main__':

	ARGSNR = len(sys.argv)

	if ARGSNR != 2 and ARGSNR != 3:
		print 'Usage:'
		print '  ' + sys.argv[0] + '   files_prefix' + '   [offset]'
		print
		sys.exit(1)


	COUNTER_STR_WIDTH = 4

	PREFIX = sys.argv[1]

	if ARGSNR == 2:
		OFFSET = 0
	if ARGSNR == 3:
		OFFSET = int(sys.argv[2])

	
	# get list of files only
	mypath = '.'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

	# get {file:modtime} dict
	file_modtime_dict = {}
	for p in onlyfiles:
		file_modtime_dict[p] = get_modtime(p)

	# are modtimes unique? if not, FU
	if not unique_values(file_modtime_dict.values()):
		sys.stderr.write("file_modtime_dict.values() not unique. i to niedobrze"+os.linesep)
		sys.stderr.write("wzorzec zmiany:"+os.linesep)
		sys.stderr.write("    touch -t 201504042045.26 SAM_4998.JPG         // [[CC]YY]MMDDhhmm[.ss]"+os.linesep)
		sys.stderr.flush()
		sys.exit(2)
		
	# sorting filenames: modtime-sorted {file:modtime} "dict" (list'o'tuples)
	modtime_sorted_dict      = sort_dict_by_val(file_modtime_dict)
	modtime_sorted_dict_keys = [entry[0] for entry in modtime_sorted_dict]	# ".keys()"

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

