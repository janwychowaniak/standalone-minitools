from pyytvidstats import scrape
from pyytvidstats import likesPercent
from pyytvidstats import findId
from pyytvidstats import isURL
from pyytvidstats import getIdsArg
from pyytvidstats import formatInfo


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


def test_isURL():

    urlSimple = 'https://www.youtube.com/watch?v=T3g9ONrwWHo'
    urlComplex = 'https://www.youtube.com/watch?v=qMliNd2b2K0&index=4&t=0s&list=PLefV978fp07exGUoyfxqXbNnjbFlhAu1n'
    notUrl = 'eujOPZRipi0'

    assert not isURL(notUrl)
    assert isURL(urlSimple)
    assert isURL(urlComplex)


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

