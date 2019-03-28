from autotag import validate_dirname
from autotag import validate_titles
from autotag import get_artist_album
from autotag import get_titles

from autotag import set_mp3_with_id3v2
from autotag import set_ogg_with_vorbiscomment




def test_validatename():

    dirname0_2 = "Artistbit1_Artistbit2_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"
    dirname0_3 = "Artistbit1_Artistbit2_-_2013_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"

    dirname1_spaces = "Artistbit1 Artistbit2 Artistbit3 - 2002 - Titlebit"

    dirname2_noDel = "Artistbit1_Artistbit2-Titlebit1_Titlebit2_Titlebit3_Titlebit4"
    dirname2_3Dels = "Artistbit1_Artistbit2_-_Titlebit1_Titlebit2_-_Titlebit3_Titlebit4_-_Titlebit5_Titlebit6_Titlebit7"

    dirname3_2ndNotYear = "Artistbit1_Artistbit2_-_2x13_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"

    assert validate_dirname(dirname0_2)
    assert validate_dirname(dirname0_3)
    
    assert not validate_dirname(dirname1_spaces)

    assert not validate_dirname(dirname2_3Dels)
    assert not validate_dirname(dirname2_noDel)
    
    assert not validate_dirname(dirname3_2ndNotYear)


def test_get_artist_album():

    dirname0_2 = "Artistbit1_Artistbit2_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"
    dirname0_3 = "Artistbit1_Artistbit2_-_2013_-_Titlebit1_Titlebit2_Titlebit3_Titlebit4"

    assert get_artist_album(dirname0_2) == ["Artistbit1_Artistbit2", "Titlebit1_Titlebit2_Titlebit3_Titlebit4"]
    assert get_artist_album(dirname0_3) == ["Artistbit1_Artistbit2", "Titlebit1_Titlebit2_Titlebit3_Titlebit4"]



def test_validatetites():

    dirlist0        = ["title_1.mp3", "title_2.mp3", "title_3.mp3"]
    dirlist1_spaces = ["title 1.mp3", "title_2.mp3", "title_3.mp3"]

    assert validate_titles(dirlist0)
    assert not validate_titles(dirlist1_spaces)


def test_get_titles():

    dirlist0        = ["title_1.mp3", "title_2.mp3", "title_3.mp3"]

    assert get_titles(dirlist0) == ["title 1", "title 2", "title 3"]


def test_set_mp3_with_id3v2():

    testcontent = \
    [['zalewski', 'wspomnienia', 1, 'A', 'A.mp3'],
     ['zalewski', 'wspomnienia', 2, 'B', 'B.mp3'],
     ['zalewski', 'wspomnienia', 3, 'C', 'C.mp3'],
     ['zalewski', 'wspomnienia', 4, 'D', 'D.mp3'],
     ['zalewski', 'wspomnienia', 5, 'E', 'E.mp3'],
     ['zalewski', 'wspomnienia', 6, 'F', 'F.mp3']]

    expected = \
    ['id3v2 -a "zalewski" -A "wspomnienia" -T 1 -t "A" A.mp3',
     'id3v2 -a "zalewski" -A "wspomnienia" -T 2 -t "B" B.mp3',
     'id3v2 -a "zalewski" -A "wspomnienia" -T 3 -t "C" C.mp3',
     'id3v2 -a "zalewski" -A "wspomnienia" -T 4 -t "D" D.mp3',
     'id3v2 -a "zalewski" -A "wspomnienia" -T 5 -t "E" E.mp3',
     'id3v2 -a "zalewski" -A "wspomnienia" -T 6 -t "F" F.mp3']

    assert set_mp3_with_id3v2(testcontent) == expected


def test_set_ogg_with_vorbiscomment():

    testcontent = \
    [['zalewski', 'wspomnienia', 1, 'A', 'A.ogg'],
     ['zalewski', 'wspomnienia', 2, 'B', 'B.ogg'],
     ['zalewski', 'wspomnienia', 3, 'C', 'C.ogg'],
     ['zalewski', 'wspomnienia', 4, 'D', 'D.ogg'],
     ['zalewski', 'wspomnienia', 5, 'E', 'E.ogg'],
     ['zalewski', 'wspomnienia', 6, 'F', 'F.ogg']]

    expected = \
    ['vorbiscomment -w A.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=1" -t "TITLE=A"',
     'vorbiscomment -w B.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=2" -t "TITLE=B"',
     'vorbiscomment -w C.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=3" -t "TITLE=C"',
     'vorbiscomment -w D.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=4" -t "TITLE=D"',
     'vorbiscomment -w E.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=5" -t "TITLE=E"',
     'vorbiscomment -w F.ogg -t "ARTIST=zalewski" -t "ALBUM=wspomnienia" -t "TRACKNUMBER=6" -t "TITLE=F"']

    assert set_ogg_with_vorbiscomment(testcontent) == expected
