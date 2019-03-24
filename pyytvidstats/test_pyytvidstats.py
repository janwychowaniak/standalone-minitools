from pyytvidstats import scrape
from pyytvidstats import likesPercent
from pyytvidstats import findId
from pyytvidstats import isURL
from pyytvidstats import Validator
from pyytvidstats import getIdsArg
from pyytvidstats import formatInfo

from pyytvidstats import BareIDParser
from pyytvidstats import VideoURLParser
from pyytvidstats import ListURLParser
from pyytvidstats import FilenameParser

from pyytvidstats import InputType
from pyytvidstats import recognizeInputType
from pyytvidstats import categorize
from pyytvidstats import extractIDs

import pytest

def test_scrape_with_1video():
    
    response_with_1video = {
        u'etag': u'"XpPGQXPnxQJhLgs6enD_n8JR4Qk/h2KHoJqEQBESg_I1dl1jyCjLWZw"',
        u'items': [{
            u'etag': u'"XpPGQXPnxQJhLgs6enD_n8JR4Qk/Uv1SH2beawj5oghFds9DCo4Yn5M"',
            u'id': u'mJw1k6RGyvQ',
            u'kind': u'youtube#video',
            u'statistics': {
                u'commentCount': u'4248',
                u'dislikeCount': u'4367',
                u'favoriteCount': u'0',
                u'likeCount': u'57384',
                u'viewCount': u'12899698'}}],
            u'kind': u'youtube#videoListResponse',
            u'pageInfo': {u'resultsPerPage': 1, u'totalResults': 1}}

    expected = [{
        u'id': u'mJw1k6RGyvQ',
        u'viewCount': 12899698,
        u'likeCount': 57384,
        u'dislikeCount': 4367
    }]

    assert scrape(response_with_1video) == expected


def test_scrape_with_2videos():

    response_with_2videos = {
        u'etag': u'"XpPGQXPnxQJhLgs6enD_n8JR4Qk/Gh_1AA-Kdxe09plffcGTy7a-Ljc"',
        u'items': [{
            u'etag': u'"XpPGQXPnxQJhLgs6enD_n8JR4Qk/Uv1SH2beawj5oghFds9DCo4Yn5M"',
            u'id': u'mJw1k6RGyvQ',
            u'kind': u'youtube#video',
            u'statistics': {
                u'commentCount': u'4248',
                u'dislikeCount': u'4367',
                u'favoriteCount': u'0',
                u'likeCount': u'57384',
                u'viewCount': u'12899698'}},
            {
            u'etag': u'"XpPGQXPnxQJhLgs6enD_n8JR4Qk/w_231iN4bK9-7V-npEGEBnKyjzc"',
            u'id': u'eujOPZRipi0',
            u'kind': u'youtube#video',
            u'statistics': {
                u'commentCount': u'501',
                u'dislikeCount': u'1611',
                u'favoriteCount': u'0',
                u'likeCount': u'9946',
                u'viewCount': u'4274250'}}],
        u'kind': u'youtube#videoListResponse',
        u'pageInfo': {u'resultsPerPage': 2, u'totalResults': 2}}

    expected = [{
        u'id': u'mJw1k6RGyvQ',
        u'viewCount': 12899698,
        u'likeCount': 57384,
        u'dislikeCount': 4367 },
    {
        u'id': u'eujOPZRipi0',
        u'viewCount': 4274250,
        u'likeCount': 9946,
        u'dislikeCount': 1611
    }]

    assert scrape(response_with_2videos) == expected


def test_likesPercent():

    videoStatsInput1 = {
        u'id': u'mJw1k6RGyvQ',
        u'viewCount': 12899698,
        u'likeCount': 57384,
        u'dislikeCount': 4367
    }

    expected1 = (92, 61751)

    assert likesPercent(videoStatsInput1) == expected1

    videoStatsInput2 = {
        u'id': u'eujOPZRipi0',
        u'viewCount': 4274250,
        u'likeCount': 9946,
        u'dislikeCount': 1611
    }

    expected2 = (86, 11557)

    assert likesPercent(videoStatsInput2) == expected2


# TODO deprecated
def test_isURL():

    urlSimple = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
    urlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'
    notUrl = 'eujOPZRipi0'

    assert isURL(urlSimple)
    assert isURL(urlComplex)
    assert not isURL(notUrl)
        


def test_findId():

    assert 'eujOPZRipi0' == findId('eujOPZRipi0')
    assert 'T3g9ONrwWHo' == findId('https://www.youtube.com/watch?v=T3g9ONrwWHo')
    assert 'qMliNd2b2K0' == findId('https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n')


def test_getIdsArg():

    urlSimple = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
    urlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'
    notUrl = 'eujOPZRipi0'

    expected = 'T3g9ONrwWHo,qMliNd2b2K0,eujOPZRipi0'

    assert getIdsArg([urlSimple, urlComplex, notUrl]) == expected


def test_formatInfo():

    assert formatInfo('eujOPZRipi0', 12899698, 94, 1234) == 'eujOPZRipi0 - 94% (1234 votes / 12899698 views)'
    assert formatInfo('T3g9ONrwWHo', 4274250, 86, 5678) == 'T3g9ONrwWHo - 86% (5678 votes / 4274250 views)'



class TestParsers(object):

    def test_BareIDParser(self):
        
        parser = BareIDParser()

        assert 'T3g9ONrwWHo' == parser.parse('T3g9ONrwWHo')
        assert '7YcW25PHnAA' == parser.parse('7YcW25PHnAA')


    def test_VideoURLParser(self):
        
        parser = VideoURLParser()

        videoUrlSimple1 = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
        videoUrlSimple2 = 'https://www.youtube.com/watch?v=7YcW25PHnAA'
        videoUrlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'

        assert 'T3g9ONrwWHo' == parser.parse(videoUrlSimple1)
        assert '7YcW25PHnAA' == parser.parse(videoUrlSimple2)
        assert 'qMliNd2b2K0' == parser.parse(videoUrlComplex)


    def test_ListURLParser(self):

        parser = ListURLParser()

        listUrlSimple1 = 'https://www.youtube.com/playlist?list=PL-fnyl58_Xju0uUwWMY6e1-zrGxjTX4ZX'
        listUrlSimple2 = 'https://www.youtube.com/playlist?list=PL-fnyl58_Xjvp8PtcS-yxW1A8y46gExQH'
        listUrlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'

        assert 'PL-fnyl58_Xju0uUwWMY6e1-zrGxjTX4ZX' == parser.parse(listUrlSimple1)
        assert 'PL-fnyl58_Xjvp8PtcS-yxW1A8y46gExQH' == parser.parse(listUrlSimple2)
        assert 'PLefV978fp07exGUoyfxqXbNnjbFlhAu1n' == parser.parse(listUrlComplex)


    def test_FilenameParser(self):

        parser = FilenameParser()

        filename1 = 'What are Microservices-j3XufmvEMiM.mkv'
        filename2 = 'Principles Of Microservices by Sam Newman-PFQnNFe27kU.mkv'
        filename3long = './Travesty_Media/20170218-Should You Learn PHP - Pros and Cons-j7upFWBKzBQ.mkv'

        assert 'j3XufmvEMiM' == parser.parse(filename1)
        assert 'PFQnNFe27kU' == parser.parse(filename2)
        assert 'j7upFWBKzBQ' == parser.parse(filename3long)



@pytest.fixture
def getv():
    return Validator()

class TestValidator():

    def test_isURL(self, getv):

        urlSimple = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
        urlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'
        notUrl = 'eujOPZRipi0'

        assert getv.isURL(urlSimple)
        assert getv.isURL(urlComplex)
        assert not getv.isURL(notUrl)


    def test_isBareID(self, getv):

        assert getv.isBareID('x9K_ByyYLOM')
        assert getv.isBareID('IUhFdI-IsVY')
        assert getv.isBareID('Q_FvLcC2-Vg')

        assert not getv.isBareID('x9K_Byy*LOM')    # disallowed character
        assert not getv.isBareID('x9K_ByyYLOMM')   # too long
        assert not getv.isBareID('x9K_ByYOMM')     # too short


    def test_isFileName(self, getv):

        valid1 = 'Principles Of Microservices by Sam Newman-PFQnNFe27kU.mkv'
        valid2 = './Travesty_Media/20170218-Should You Learn PHP - Pros and Cons-j7upFWBKzBQ.mkv'
        valid3 = 'Box Sizing _ Beginner\'s Course _ #10-dLGr1Qb2nKc.webm'
        valid4 = 'PHP Tutorial (& MySQL) #10 - Booleans & Comparisons-hxYQA-nuIXY.mp4'
        valid5 = 'Box Sizing _ Beginner\'s Course _ #10-dLGr1Qb2nKc.WEBM'

        assert getv.isFileName(valid1)
        assert getv.isFileName(valid2)
        assert getv.isFileName(valid3)
        assert getv.isFileName(valid4)
        assert getv.isFileName(valid5)

        invalid1 = 'Principles Of Microservices by Sam Newman-PFQnNFe27kU.doc'  # wrong file type
        invalid2 = 'Principles Of Microservices by Sam Newman.mkv'              # no ID at the end

        assert not getv.isFileName(invalid1)
        assert not getv.isFileName(invalid2)



def test_recognizeInputType():

    validator = Validator()
    
    # bare ID
    bareID = 'eujOPZRipi0'

    # video URLs
    videoUrl1 = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
    videoUrl2 = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'

    # list URLs
    listUrl1 = 'https://www.youtube.com/playlist?list=PL-fnyl58_Xju0uUwWMY6e1-zrGxjTX4ZX'
    listUrl2 = 'https://www.youtube.com/watch?index=4&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n&t=0s'

    # file names
    filename1 = './Travesty_Media/20170218-Should You Learn PHP - Pros and Cons-j7upFWBKzBQ.mkv'
    filename2 = 'PHP Tutorial (& MySQL) #10 - Booleans & Comparisons-hxYQA-nuIXY.mp4'
    filename3 = 'Box Sizing _ Beginner\'s Course _ #10-dLGr1Qb2nKc.WEBM'

    # none of the above
    garbage1 = 'Lorem ipsum dolor sit amet'


    assert recognizeInputType(validator, bareID) == InputType.BAREID

    assert recognizeInputType(validator, videoUrl1) == InputType.URLVIDEO
    assert recognizeInputType(validator, videoUrl2) == InputType.URLVIDEO

    assert recognizeInputType(validator, listUrl1) == InputType.URLLIST
    assert recognizeInputType(validator, listUrl2) == InputType.URLLIST

    assert recognizeInputType(validator, filename1) == InputType.FILENAME
    assert recognizeInputType(validator, filename2) == InputType.FILENAME
    assert recognizeInputType(validator, filename3) == InputType.FILENAME

    assert not recognizeInputType(validator, garbage1)


def test_categorize():

    # "_args" below is what may actually come from the commandline
    _args = ['eujOPZRipi0',                                   # bare ID
             'https://www.youtube.com/watch?v=T3g9ONrwWHo',   # video URL
             'https://www.youtube.com/watch?v=T3g9ONrwWHo',   # video URL (duplicate)
             'Principles Of Microservices-PFQnNFe27kU.mkv',   # file
             'Lorem']                                         # garbage

    expected = {'eujOPZRipi0' : InputType.BAREID,
                'https://www.youtube.com/watch?v=T3g9ONrwWHo' : InputType.URLVIDEO,
                'Principles Of Microservices-PFQnNFe27kU.mkv' : InputType.FILENAME, }
                # 'Lorem': None}

    assert expected == categorize(Validator(), _args)


def test_extractIDs():

    _args = {'eujOPZRipi0' : InputType.BAREID,
             'https://www.youtube.com/watch?v=T3g9ONrwWHo' : InputType.URLVIDEO,
             'Principles Of Microservices-PFQnNFe27kU.mkv' : InputType.FILENAME, }

    expected = ['eujOPZRipi0',
                'PFQnNFe27kU',
                'T3g9ONrwWHo']

    assert expected == extractIDs(_args)
