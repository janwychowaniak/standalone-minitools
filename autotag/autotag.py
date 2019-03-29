#!/usr/bin/python



import os
import sys


USAGEMSG = \
'''
{}  mp3/ogg

    The script helps automate a somehow tedious task of
    setting ID3/Vorbis tags in the MP3 and vorbis OGG files.
    The required data is gathered from the names of
    the files and the name of the directory they reside in.

    Preferred directory naming schemes:
     XXXXX_-_YYYYY
     XXXXX_-_2000_-_YYYYY

'''


DELIMITER = "_-_"


def validate_dirname(_name):

    errmsg = ""
    # has spaces
    if _name.find(" ") != -1:
        errmsg = "Whitespaces present somewhere in the directory name"
    # has 2 delims
    if not (_name.count(DELIMITER) == 1 or _name.count(DELIMITER) == 2):
        errmsg = "Wrong number of delimiters"
    # if 2 delims, second is year
    if _name.count(DELIMITER) == 2:
        try:
            int(_name.split(DELIMITER)[1])
        except ValueError as ex:
            errmsg = "section no2 NaN"
    if errmsg:
        sys.stderr.write(errmsg + "\n") ; sys.stderr.flush()
        return False
    else:
        return True



def validate_titles(_dirlist):

    for title in _dirlist:
        # has spaces
        if title.find(" ") != -1:
            return False
    return True
    
    
    
def get_artist_album(_dirname):

    spl = _dirname.split(DELIMITER)
    if _dirname.count(DELIMITER) == 1:
        return spl
    if _dirname.count(DELIMITER) == 2:
        return [spl[0], spl[2]]
    


def get_titles(_dirlist):

    titles = []
    for title in _dirlist:
        # Get rid of the extension
        t1 = title.rsplit('.', 1)[0]
        t2 = t1.replace('_', ' ')
        titles.append(t2)
    return titles
        


def set_mp3_with_id3v2(content):

    commands = []
    for t in content:
        commands.append('id3v2 -a "{}" -A "{}" -T {} -t "{}" {}'
            .format(t[0], t[1], t[2], t[3], t[4]))
    return commands


def set_ogg_with_vorbiscomment(content):

    commands = []
    for t in content:
        commands.append('vorbiscomment -w {} -t "ARTIST={}" -t "ALBUM={}" -t "TRACKNUMBER={}" -t "TITLE={}"'
            .format(t[4], t[0], t[1], t[2], t[3]))
    return commands


# ------------------------------------------------------------------------


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write(USAGEMSG.format(sys.argv[0]))
        sys.exit(1)

    EXT = sys.argv[1]

    
    dir_name        = os.getcwd().split('/')[-1]
    dir_listing_ext = filter(lambda s: s.endswith(EXT), sorted(os.listdir('.')))
    
    
    valid_d = validate_dirname(dir_name)
    valid_t = validate_titles(dir_listing_ext)
    
    if not valid_d:
        sys.stderr.write("something wrong with the directory name\n") ; sys.stderr.flush()
        sys.exit(1)
    
    if not valid_t:
        sys.stderr.write("something wrong with the file names\n") ; sys.stderr.flush()
        sys.exit(2)
    
    
    artist, album = get_artist_album(dir_name)
    titles = get_titles(dir_listing_ext)

    content = []
    nr = 1
    for titles_n_files in zip(titles, dir_listing_ext):
        content.append([artist, album, nr, titles_n_files[0], titles_n_files[1]])
        nr+=1


    if EXT == 'mp3':
        # print '# --- set_mp3_with_id3v2 --- '
        print
        for cmd in set_mp3_with_id3v2(content): print cmd
        print
    elif EXT == 'ogg':
        # print '# --- set_ogg_with_vorbiscomment --- '
        print
        for cmd in set_ogg_with_vorbiscomment(content): print cmd
        print
    else:
        print ' *** The filetype given is neither "mp3" nor "ogg"'

