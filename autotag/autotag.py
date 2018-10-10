#!/usr/bin/python



import os
import sys


DELIMITER = "_-_"


def validate_dirname(_name):
    errmsg = ""
    # has spaces
    if _name.find(" ") != -1:
        errmsg = "spacje gdzies w nazwie"
    # has 2 delims
    if not (_name.count(DELIMITER) == 1 or _name.count(DELIMITER) == 2):
        errmsg = "zla liczba delimiterow"
    # if 2 delims, second is year
    if _name.count(DELIMITER) == 2:
        try:
            int(_name.split(DELIMITER)[1])
        except ValueError as ex:
            errmsg = "delimiter 2 nienumryczny"
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
        # upierdol rozszerzenie
        t1 = title.rsplit('.', 1)[0]
        t2 = t1.replace('_', ' ')
        titles.append(t2)
    return titles
        
    

# ////////////////////////////////////////////////////////////////////////
# for py.test
# ------------------

dirname0_3 = "Artistbit1_Artistbit2_-_2013_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"
dirname0_2 = "Artistbit1_Artistbit2_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"

dirname1_spaces = "Artistbit1 Artistbit2 Artistbit3 - 2002 - Titlebit"

dirname2_noDel = "Artistbit1_Artistbit2-Titlebit1_Titlebit2_Titlebit3_Titlebit4"
dirname2_3Dels = "Artistbit1_Artistbit2_-_Titlebit1_Titlebit2_-_Titlebit3_Titlebit4_-_Titlebit5_Titlebit6_Titlebit7"

dirname3_2ndNotYear = "Artistbit1_Artistbit2_-_2x13_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"


def test_validatename():

    assert validate_dirname(dirname0_2) == True
    assert validate_dirname(dirname0_3) == True
    
    assert validate_dirname(dirname1_spaces) == False

    assert validate_dirname(dirname2_3Dels) == False
    assert validate_dirname(dirname2_noDel) == False
    
    assert validate_dirname(dirname3_2ndNotYear) == False


# ------------------

dirlist0        = ["title_1.mp3", "title_2.mp3", "title_3.mp3"]
dirlist1_spaces = ["title 1.mp3", "title_2.mp3", "title_3.mp3"]


def test_validatetites():

    assert validate_titles(dirlist0) == True
    assert validate_titles(dirlist1_spaces) == False

# ------------------

def test_get_artist_album():
    assert get_artist_album(dirname0_2) == ["Artistbit1_Artistbit2", "Titlebit1_Titlebit2_Titlebit3_Titlebit4"]
    assert get_artist_album(dirname0_3) == ["Artistbit1_Artistbit2", "Titlebit1_Titlebit2_Titlebit3_Titlebit4"]

# ------------------

def test_get_titles():
    assert get_titles(dirlist0) == ["title 1", "title 2", "title 3"]

# ////////////////////////////////////////////////////////////////////////


def set_mp3_with_id3v2(content):
    print
#    # clear tags
#    print 'id3v2 -D *.mp3'
    # set
    for t in content:
        print 'id3v2 -a "%s" -A "%s" -T %d -t "%s" %s' % (t[0], t[1], t[2], t[3], t[4])
    print


def set_ogg_with_vorbiscomment(content):
    print
    # set
    for t in content:
        print 'vorbiscomment -w %s -t "ARTIST=%s" -t "ALBUM=%s" -t "TRACKNUMBER=%d" -t "TITLE=%s"' % (t[4], t[0], t[1], t[2], t[3])
    print


# ------------------------------------------------------------------------


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        sys.stderr.write('Usage:')                                                         ; sys.stderr.flush()
        sys.stderr.write('  %s   ext' % sys.argv[0]) ; sys.stderr.flush()
        sys.stderr.write('\n')                                                             ; sys.stderr.flush()
        sys.exit(1)

    EXT = sys.argv[1]

    
    dir_name        = os.getcwd().split('/')[-1]
    dir_listing_ext = filter(lambda s: s.endswith(EXT), sorted(os.listdir('.')))
    
    
    valid_d = validate_dirname(dir_name)
    valid_t = validate_titles(dir_listing_ext)
    
    if not valid_d:
        sys.stderr.write("cos nie tak z nazwa folderu\n") ; sys.stderr.flush()
        sys.exit(1)
    
    if not valid_t:
        sys.stderr.write("cos nie tak z nazwami plikow\n") ; sys.stderr.flush()
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
        set_mp3_with_id3v2(content)
    elif EXT == 'ogg':
        # print '# --- set_ogg_with_vorbiscomment --- '
        set_ogg_with_vorbiscomment(content)
    else:
        print 'Nie jest to "mp3" ani "ogg"'

